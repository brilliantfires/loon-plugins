/*
 * Based on the user-supplied Keywos wyres.js dated 2025-02-19.
 * Original reference https://raw.githubusercontent.com/Keywos/rule/main/script/wy/js/wyres.js
 * Rule authors RuCu6 and Keywos. Local maintenance by Codex.
 * Loon 3.5.1(998). Uses the native AES and gzip APIs.
 */

(() => {
  function main() {
    if (typeof $request === "undefined" || typeof $response === "undefined")
      return {};
    const match = $request.url.match(
      /^https?:\/\/interface\d?\.music\.163\.com\/eapi(\/[^?]*)/i,
    );
    if (
      !match ||
      !($response.body instanceof Uint8Array) ||
      !$response.body.length
    )
      return {};

    let supplied = typeof $argument === "undefined" ? {} : $argument;
    if (typeof supplied === "string") supplied = JSON.parse(supplied || "{}");
    supplied = supplied || {};
    const enabled = (name, fallback = false) =>
      supplied[name] === undefined
        ? fallback
        : supplied[name] === true ||
          supplied[name] === 1 ||
          supplied[name] === "1" ||
          supplied[name] === "true";

    const path = match[1];
    const homePaths = [
      "/homepage/block/page",
      "/link/page/rcmd/resource/show",
      "/link/page/rcmd/block/resource/multi/refresh",
    ];
    const commentsPaths = ["/batch", "/v2/resource/comment/floor/get"];
    if (homePaths.includes(path) && !enabled("homeClean", true)) return {};
    if (commentsPaths.includes(path) && !enabled("commentsClean", true))
      return {};
    if (
      path === "/link/page/discovery/resource/show" &&
      !enabled("discoveryClean", true)
    )
      return {};
    if (
      path === "/link/position/show/resource" &&
      !enabled("myPageClean", true)
    )
      return {};
    if (
      path === "/user/follow/users/mixed/get/v2" &&
      !enabled("showUnfollowed")
    )
      return {};
    if (
      path === "/link/home/framework/tab" &&
      !["MY", "DT", "FX"].some((name) => enabled(name))
    )
      return {};
    const supported = [
      ...homePaths,
      ...commentsPaths,
      "/link/page/discovery/resource/show",
      "/link/position/show/resource",
      "/user/follow/users/mixed/get/v2",
      "/link/home/framework/tab",
    ];
    if (!supported.includes(path)) return {};

    const encoder = new TextEncoder();
    const aesOptions = {
      mode: "ecb",
      padding: "pkcs7",
      key: encoder.encode("e82ckenh8dichen8"),
    };
    let plaintext = $crypto.aes.decrypt($response.body, aesOptions);
    // Preserve compression inside the encrypted payload independently of HTTP headers.
    const compressed = plaintext[0] === 0x1f && plaintext[1] === 0x8b;
    if (compressed) plaintext = $utils.ungzip(plaintext);
    const original = new TextDecoder("utf-8").decode(plaintext);
    const data = JSON.parse(original);
    if (!data || typeof data !== "object") return {};

    const homeBlocks = {
      PRGG: "PAGE_RECOMMEND_GREETING",
      PRRK: "PAGE_RECOMMEND_RANK",
      PRDRD: "PAGE_RECOMMEND_DAILY_RECOMMEND",
      PRSCVPT: "PAGE_RECOMMEND_SPECIAL_CLOUD_VILLAGE_PLAYLIST",
      PRST: "PAGE_RECOMMEND_SHORTCUT",
      PRRR: "PAGE_RECOMMEND_RADAR",
      HMPR: "HOMEPAGE_MUSIC_PARTNER",
      PRMST: "PAGE_RECOMMEND_MY_SHEET",
      PRCN: "PAGE_RECOMMEND_COMBINATION",
    };
    const retainedBlocks = Object.entries(homeBlocks)
      .filter(([name]) => !enabled(name, name === "PRGG"))
      .map(([, code]) => code);

    switch (path) {
      case "/batch": {
        const tips = data["/api/comment/tips/v2/get"];
        if (tips?.data) tips.data = { count: 0, offset: 0, records: [] };
        const socialAds = data["/api/social/event/bff/ad/resources"];
        if (socialAds?.data) socialAds.data = {};
        const ads = data["/api/ad/get"];
        if (ads?.data) ads.data = { code: 200, ads: {} };
        cleanComments(data["/api/v2/resource/comments"]?.data?.comments);
        const inserted = data["/api/comment/feed/inserted/resources"];
        if (inserted?.data) {
          inserted.data = {};
          if (inserted.trp?.rules) inserted.trp.rules = [];
        }
        const topics = data["/api/event/rcmd/topic/list"]?.data;
        if (topics?.topicList) topics.topicList = [];
        const order =
          data["/api/platform/song/bff/grading/song/order/entrance"]?.data;
        if (order?.songOrderEntrance) order.songOrderEntrance = {};
        break;
      }
      case "/v2/resource/comment/floor/get": {
        const owner = data.data?.ownerComment;
        if (owner?.user) {
          owner.user.vipRights = null;
          owner.user.avatarDetail = {};
          owner.pendantData = null;
        }
        cleanComments(data.data?.comments);
        break;
      }
      case "/homepage/block/page":
        if (Array.isArray(data.data?.blocks)) {
          for (const block of data.data.blocks) {
            if (
              block?.showType === "BANNER" &&
              Array.isArray(block.extInfo?.banners)
            ) {
              block.extInfo.banners = block.extInfo.banners.filter(
                (banner) => !["活动", "广告"].includes(banner?.typeTitle),
              );
            }
          }
        }
        break;
      case "/link/page/rcmd/resource/show":
        if (Array.isArray(data.data?.blocks)) {
          data.data.blocks = data.data.blocks.filter((block) =>
            retainedBlocks.includes(block?.bizCode),
          );
        }
        filterBlockOrder(data.data, retainedBlocks);
        break;
      case "/link/page/rcmd/block/resource/multi/refresh":
        if (Array.isArray(data.data)) {
          data.data = data.data.filter((block) =>
            retainedBlocks.includes(block?.blockCode),
          );
        }
        break;
      case "/link/page/discovery/resource/show":
        if (Array.isArray(data.data?.blocks)) {
          data.data.blocks = data.data.blocks.filter(
            (block) => block?.bizCode !== "PAGE_DISCOVERY_BANNER",
          );
        }
        filterBlockOrder(data.data, null);
        break;
      case "/link/position/show/resource":
        if (data.data?.crossPlatformResource?.positionCode === "MyPageBar") {
          data.data.crossPlatformResource = {};
        }
        break;
      case "/link/home/framework/tab": {
        const hiddenTitles = { MY: "漫游", DT: "笔记", FX: "发现" };
        const hidden = Object.entries(hiddenTitles)
          .filter(([name]) => enabled(name))
          .map(([, title]) => title);
        if (Array.isArray(data.data?.commonResourceList)) {
          data.data.commonResourceList = data.data.commonResourceList.filter(
            (tab) => !hidden.includes(tab?.title),
          );
        }
        break;
      }
      case "/user/follow/users/mixed/get/v2":
        if (Array.isArray(data.data?.records)) {
          for (const record of data.data.records) {
            if (record?.mutualFollowDay === null) {
              record.showContent = {
                message: "💢他/她,未关注你",
                time: 1e12,
                active: true,
                boxContent: {},
              };
            }
          }
        }
        break;
    }

    const updated = JSON.stringify(data);
    // Avoid re-encrypting responses where no JSON content changed.
    if (updated === JSON.stringify(JSON.parse(original))) return {};
    let output = encoder.encode(updated);
    if (compressed) output = $utils.gzip(output);
    return { body: $crypto.aes.encrypt(output, aesOptions).ciphertext };
  }

  function cleanComments(comments) {
    if (!Array.isArray(comments)) return;
    for (const comment of comments) {
      if (!comment || typeof comment !== "object") continue;
      if (comment.user) {
        comment.user.vipRights = null;
        comment.user.avatarDetail = null;
      }
      comment.userBizLevels = null;
      comment.pendantData = null;
      if (comment.tag) {
        comment.tag.extDatas = [];
        comment.tag.contentPicDatas = null;
      }
    }
  }

  function filterBlockOrder(data, retained) {
    if (typeof data?.blockCodeOrderList !== "string") return;
    try {
      const order = JSON.parse(data.blockCodeOrderList);
      if (!Array.isArray(order)) return;
      data.blockCodeOrderList = JSON.stringify(
        order.filter((code) =>
          retained ? retained.includes(code) : code !== "PAGE_DISCOVERY_BANNER",
        ),
      );
    } catch {
      // An unrecognized ordering field can remain alongside the cleaned block list.
    }
  }

  let result = {};
  try {
    result = main();
  } catch (error) {
    console.log("网易云音乐处理失败，保留原响应。" + error.message);
  }
  $done(result);
})();
