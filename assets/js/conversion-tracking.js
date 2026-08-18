(function () {
  'use strict';

  function sendEvent(name, params) {
    params = params || {};
    params.page_path = location.pathname;
    params.page_title = document.title;

    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params);
      return;
    }

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: name }, params));
  }

  function closestLink(target) {
    return target && target.closest ? target.closest('a') : null;
  }

  function buildRfqlink() {
    var url = new URL('https://www.ajinnetworks.co.kr/');
    url.searchParams.set('utm_source', 'ajin_blog');
    url.searchParams.set('utm_medium', 'organic_content');
    url.searchParams.set('utm_campaign', 'rfq_conversion');
    url.searchParams.set('utm_content', location.pathname);
    url.searchParams.set('ajin_ref_title', document.title.slice(0, 120));
    return url.toString();
  }

  function injectRfQcta() {
    var article = document.querySelector('.post-body-wrap');
    if (!article || article.querySelector('[data-phase36-rfq]')) return;

    var box = document.createElement('section');
    box.setAttribute('data-phase36-rfq', 'true');
    box.style.cssText = 'margin:42px 0 10px;padding:24px;border:1px solid #d9e2ec;border-radius:14px;background:#f7f9fc;';
    box.innerHTML = '<h2 style="margin:0 0 10px;padding:0;border:0;font-size:1.25rem;">자동화 기술검토·RFQ 상담</h2>' +
      '<p style="margin:0 0 14px;line-height:1.7;">제품 도면 또는 Sample, 현재 공정 Cycle Time, 목표 CAPA, 설치공간과 기존 PLC·Robot·Vision 사양이 있으면 기술검토 범위를 더 정확하게 산정할 수 있습니다.</p>' +
      '<a data-conversion-kind="rfq" data-source-type="blog-post" data-source-topic="' + encodeURIComponent(document.title) + '" href="' + buildRfqlink() + '" style="display:inline-block;padding:11px 18px;border-radius:8px;background:#153b6b;color:#fff;text-decoration:none;border:0;font-weight:700;">아진네트웍스 기술상담 요청</a>';

    var tags = article.querySelector('.post-tags');
    if (tags) article.insertBefore(box, tags);
    else article.appendChild(box);
  }

  document.addEventListener('DOMContentLoaded', injectRfQcta);

  document.addEventListener('click', function (event) {
    var link = closestLink(event.target);
    if (!link) return;

    var kind = link.getAttribute('data-conversion-kind');
    if (kind === 'rfq') {
      sendEvent('rfq_cta_click', {
        source_type: link.getAttribute('data-source-type') || 'post',
        source_topic: decodeURIComponent(link.getAttribute('data-source-topic') || ''),
        destination: link.href
      });
      return;
    }

    var article = link.closest('.post-body-wrap');
    if (article && link.hostname === location.hostname && /^\/\d{4}\/\d{2}\/\d{2}\//.test(link.pathname)) {
      sendEvent('pillar_cluster_click', {
        link_role: 'internal_content',
        destination_path: link.pathname,
        anchor_text: (link.textContent || '').trim().slice(0, 100)
      });
      return;
    }

    if (link.hostname === 'www.ajinnetworks.co.kr') {
      sendEvent('company_site_click', {
        destination: link.href,
        anchor_text: (link.textContent || '').trim().slice(0, 100)
      });
    }
  }, { passive: true });
})();
