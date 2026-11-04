/*
 * Based on the user-supplied RuCu6 script dated 2024-01-12.
 * Original reference https://raw.githubusercontent.com/RuCu6/QuanX/main/Scripts/myBlockAds.js
 * Local maintenance by Codex.
 */

(() => {
  function main() {
    if (typeof $request === "undefined" || typeof $response === "undefined") return {};
    if (typeof $response.body !== "string" || !$response.body) return {};

    const url = $request.url;
    const video = /^https:\/\/guide-acs\.m\.taobao\.com\/gw\/mtop\.taobao\.cloudvideo\.video\.query/i.test(url);
    const image = /^https:\/\/guide-acs\.m\.taobao\.com\/gw\/mtop\.taobao\.wireless\.home\.splash\.awesome\.get/i.test(url);
    const activity = /^https:\/\/poplayer\.template\.alibaba\.com\/\w+\.json/i.test(url);
    if (!video && !image && !activity) return {};

    const data = JSON.parse($response.body);
    if (!data || typeof data !== "object" || Array.isArray(data)) return {};
    const original = JSON.stringify(data);

    if (video) {
      if (data.data && typeof data.data === "object" && !Array.isArray(data.data)) {
        if (data.data.duration) data.data.duration = "0";
        if (Array.isArray(data.data.resources) && data.data.resources.length) data.data.resources = [];
        if (Array.isArray(data.data.caches) && data.data.caches.length) data.data.caches = [];
        if (data.data.respTimeInMs) data.data.respTimeInMs = "3818332800000";
      }
    } else if (image) {
      const sections = data.data?.containers?.splash_home_base?.base?.sections;
      if (Array.isArray(sections)) {
        for (const section of sections) {
          const items = section?.bizData?.["taobao-splash"]?.data;
          if (!Array.isArray(items)) continue;
          for (const item of items) {
            if (!item || typeof item !== "object" || Array.isArray(item)) continue;
            Object.assign(item, {
              waitTime: "0",
              times: "0",
              hotStart: "false",
              haveVoice: "false",
              hideTBLogo: "false",
              enable4G: "false",
              coldStart: "false",
              startTime: "3818332800000",
              endTime: "3818419199000",
              gmtStart: "2090-12-31 00:00:00",
              gmtEnd: "2090-12-31 23:59:59",
              gmtStartMs: "3818332800000",
              gmtEndMs: "3818419199000",
            });
            if (item.imgUrl) item.imgUrl = "";
            if (item.videoUrl) item.videoUrl = "";
          }
        }
      }
    } else {
      if (Array.isArray(data.res?.images) && data.res.images.length) data.res.images = [];
      if (Array.isArray(data.res?.videos) && data.res.videos.length) data.res.videos = [];
      if (data.enable) data.enable = false;
      if (Array.isArray(data.mainRes?.images) && data.mainRes.images.length) data.mainRes.images = [];
    }

    const body = JSON.stringify(data);
    return body === original ? {} : { body };
  }

  let result = {};
  try {
    result = main();
  } catch (error) {
    console.log("淘宝开屏处理失败，保留原响应。" + error.message);
  }
  $done(result);
})();
