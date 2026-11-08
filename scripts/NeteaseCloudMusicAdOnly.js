/*
 * NetEase Cloud Music in-app ad cleanup for the lite InApp-Ads plugin.
 *
 * Only two AES-ECB/gzip response endpoints are handled:
 * - /eapi/link/page/rcmd/resource/show: remove explicit VIP promotion banners.
 * - /eapi/link/scene/show/resource: remove the home global popup that carries
 *   VIP_SUBSCRIBE_PROMOTION, while retaining unrelated hints and medal popups.
 */

(() => {
  const HANDLED_PATHS = new Set([
    "/eapi/link/page/rcmd/resource/show",
    "/eapi/link/scene/show/resource",
  ]);
  const AES_KEY = "e82ckenh8dichen8";

  function main() {
    if (typeof $request === "undefined" || typeof $response === "undefined")
      return {};
    if (
      !$response ||
      !($response.body instanceof Uint8Array) ||
      !$response.body.length
    )
      return {};

    let path = "";
    try {
      path = new URL($request.url).pathname;
    } catch {
      return {};
    }
    if (!HANDLED_PATHS.has(path)) return {};

    const encoder = new TextEncoder();
    const decoder = new TextDecoder();
    const aesOptions = {
      mode: "ecb",
      padding: "pkcs7",
      key: encoder.encode(AES_KEY),
    };

    try {
      let plaintext = $crypto.aes.decrypt($response.body, aesOptions);
      const compressed =
        plaintext.length >= 2 &&
        plaintext[0] === 0x1f &&
        plaintext[1] === 0x8b;
      if (compressed) plaintext = $utils.ungzip(plaintext);

      const original = decoder.decode(plaintext);
      const data = JSON.parse(original);
      if (!data || typeof data !== "object" || Array.isArray(data)) return {};

      const changed =
        path === "/eapi/link/page/rcmd/resource/show"
          ? removeHomePromotionBanners(data)
          : removeVipGlobalPopup(data);
      if (!changed) return {};

      const updated = JSON.stringify(data);
      if (updated === JSON.stringify(JSON.parse(original))) return {};

      let output = encoder.encode(updated);
      if (compressed) output = $utils.gzip(output);
      return { body: $crypto.aes.encrypt(output, aesOptions).ciphertext };
    } catch {
      return {};
    }
  }

  function removeHomePromotionBanners(data) {
    const page = asObject(data.data);
    if (!page || !Array.isArray(page.blocks)) return false;

    const removedCodes = new Set();
    let changed = false;
    page.blocks = page.blocks.filter((block) => {
      if (!isObject(block)) return true;
      const code = stringValue(block.positionCode || block.bizCode);
      const banners = asObject(block.nativeData)?.banners;
      if (!/^PAGE_RECOMMEND_BANNER_\d+$/.test(code) || !Array.isArray(banners))
        return true;

      const kept = banners.filter((banner) => !isExplicitPromotionBanner(banner));
      if (kept.length === banners.length) return true;
      changed = true;
      if (kept.length) {
        block.nativeData.banners = kept;
        return true;
      }
      removedCodes.add(code);
      return false;
    });

    if (!changed) return false;
    removeCodesFromJsonString(page, "blockCodeOrderList", removedCodes);
    removeCodesFromJsonString(page, "requestBlockOrder", removedCodes);
    return true;
  }

  function isExplicitPromotionBanner(banner) {
    if (!isObject(banner)) return false;
    if (banner.showAdTag === true) return true;

    const typeTitle = stringValue(banner.typeTitle);
    if (typeTitle === "广告" || typeTitle === "活动") return true;
    if (banner.bannerType === "force_banner") return true;

    const marker = [
      banner.fromId,
      banner.s_ctrp,
      banner.scm,
      banner.log?.s_ctrp,
    ]
      .filter((value) => typeof value === "string")
      .join(" ");
    return /VIP_SUBSCRIBE_PROMOTION|starlink_revenue/i.test(marker);
  }

  function removeVipGlobalPopup(data) {
    const page = asObject(data.data);
    if (!page || !Array.isArray(page.hints)) return false;

    const removedCodes = new Set();
    let changed = false;
    page.hints = page.hints.filter((hint) => {
      if (!isVipGlobalPopupHint(hint)) return true;
      changed = true;
      const code = stringValue(hint?.code);
      if (code) removedCodes.add(code);
      for (const resourceCode of hint?.resourceCodes || []) {
        const value = stringValue(resourceCode?.resourceCode);
        if (value) removedCodes.add(value);
      }
      return false;
    });
    if (!changed) return false;

    const trp = asObject(data.trp);
    if (trp && Array.isArray(trp.rules)) {
      trp.rules = trp.rules.filter(
        (rule) =>
          typeof rule !== "string" ||
          (!/HOME_MID_POPUP|homeMidPopUp/i.test(rule) &&
            ![...removedCodes].some((code) => rule.includes(code))),
      );
    }
    return true;
  }

  function isVipGlobalPopupHint(hint) {
    if (!isObject(hint)) return false;
    const code = stringValue(hint.code);
    if (/homeMidPopUp/i.test(code)) return true;

    const payload = asObject(hint.data);
    if (!payload) return false;
    const channel = stringValue(payload.channelCode);
    if (/homeMidPopUp/i.test(channel)) return true;

    const text = safeStringify(payload);
    return /VIP_SUBSCRIBE_PROMOTION|homeMidPopUpDataChannel|supervipday/i.test(
      text,
    );
  }

  function removeCodesFromJsonString(container, key, removedCodes) {
    if (!removedCodes.size || typeof container[key] !== "string") return;
    try {
      const list = JSON.parse(container[key]);
      if (!Array.isArray(list)) return;
      container[key] = JSON.stringify(
        list.filter((code) => !removedCodes.has(stringValue(code))),
      );
    } catch {
      // Leave an unknown ordering format untouched.
    }
  }

  function safeStringify(value) {
    try {
      return JSON.stringify(value);
    } catch {
      return "";
    }
  }

  function stringValue(value) {
    return typeof value === "string" ? value : "";
  }

  function isObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function asObject(value) {
    return isObject(value) ? value : null;
  }

  return main();
})();
