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

  document.addEventListener('click', function (event) {
    var link = closestLink(event.target);
    if (!link) return;

    var kind = link.getAttribute('data-conversion-kind');
    if (kind === 'rfq') {
      sendEvent('rfq_cta_click', {
        source_type: link.getAttribute('data-source-type') || 'post',
        source_topic: link.getAttribute('data-source-topic') || '',
        destination: link.href
      });
      return;
    }

    if (kind === 'pillar-cluster') {
      sendEvent('pillar_cluster_click', {
        link_role: link.getAttribute('data-link-role') || 'internal',
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
