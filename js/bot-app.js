/**
 * RC Marketing Bot - Application Logic
 * Store, Compliance, Generator, Views, Nav, Event Handlers
 */

(function () {
  'use strict';

  // ── Store: localStorage CRUD ───────────────────────────────────────────────
  var Store = {
    KEYS: { calendar: 'rc_bot_calendar', content: 'rc_bot_content', initialized: 'rc_bot_init' },

    init: function () {
      if (!localStorage.getItem(Store.KEYS.initialized)) {
        Store.seed();
      }
    },

    seed: function () {
      localStorage.setItem(Store.KEYS.calendar, JSON.stringify(BOT_DATA.seedCalendar));
      localStorage.setItem(Store.KEYS.content, JSON.stringify(BOT_DATA.seedContent));
      localStorage.setItem(Store.KEYS.initialized, '1');
    },

    reset: function () {
      localStorage.removeItem(Store.KEYS.calendar);
      localStorage.removeItem(Store.KEYS.content);
      localStorage.removeItem(Store.KEYS.initialized);
      Store.seed();
      Nav.toast('Data reset to defaults');
      Nav.switchView('dashboard');
    },

    getCalendar: function () {
      return JSON.parse(localStorage.getItem(Store.KEYS.calendar) || '[]');
    },

    saveCalendar: function (items) {
      localStorage.setItem(Store.KEYS.calendar, JSON.stringify(items));
    },

    addCalendarEntry: function (entry) {
      var items = Store.getCalendar();
      entry.id = 'cal-' + Date.now();
      entry.status = 'draft';
      items.push(entry);
      Store.saveCalendar(items);
      return entry;
    },

    updateCalendarEntry: function (id, updates) {
      var items = Store.getCalendar();
      for (var i = 0; i < items.length; i++) {
        if (items[i].id === id) {
          Object.keys(updates).forEach(function (k) { items[i][k] = updates[k]; });
          break;
        }
      }
      Store.saveCalendar(items);
    },

    deleteCalendarEntry: function (id) {
      var items = Store.getCalendar().filter(function (e) { return e.id !== id; });
      Store.saveCalendar(items);
    },

    getContent: function () {
      return JSON.parse(localStorage.getItem(Store.KEYS.content) || '[]');
    },

    saveContent: function (items) {
      localStorage.setItem(Store.KEYS.content, JSON.stringify(items));
    },

    addContent: function (item) {
      var items = Store.getContent();
      item.id = 'content-' + Date.now();
      item.created = new Date().toISOString().slice(0, 10);
      item.published = null;
      item.metrics = null;
      items.push(item);
      Store.saveContent(items);
      return item;
    },

    updateContent: function (id, updates) {
      var items = Store.getContent();
      for (var i = 0; i < items.length; i++) {
        if (items[i].id === id) {
          Object.keys(updates).forEach(function (k) { items[i][k] = updates[k]; });
          break;
        }
      }
      Store.saveContent(items);
    },

    getContentById: function (id) {
      return Store.getContent().find(function (c) { return c.id === id; }) || null;
    }
  };

  // ── Compliance: check content against brand rules ──────────────────────────
  var Compliance = {
    check: function (text) {
      var issues = [];
      var lower = text.toLowerCase();
      BOT_DATA.forbiddenTerms.forEach(function (term) {
        if (lower.indexOf(term.toLowerCase()) !== -1) {
          issues.push('Contains forbidden term: "' + term + '"');
        }
      });
      // Length checks
      if (text.length > 5000) {
        issues.push('Content exceeds 5,000 characters (' + text.length + ')');
      }
      if (text.length < 50) {
        issues.push('Content is too short (minimum 50 characters)');
      }
      return { pass: issues.length === 0, issues: issues };
    },

    renderBadge: function (text) {
      var result = Compliance.check(text);
      return '<span class="bot-badge ' + (result.pass ? 'bot-badge-pass' : 'bot-badge-fail') + '">' + (result.pass ? 'Pass' : 'Fail') + '</span>';
    },

    renderDetail: function (text) {
      var result = Compliance.check(text);
      var html = '<p>' + Compliance.renderBadge(text) + '</p>';
      if (result.pass) {
        html += '<p style="font-size:14px;color:var(--muted);margin-top:8px;">No compliance issues detected.</p>';
      } else {
        html += '<ul style="margin-top:8px;padding-left:20px;">';
        result.issues.forEach(function (issue) {
          html += '<li style="font-size:14px;color:#991b1b;margin-bottom:4px;">' + issue + '</li>';
        });
        html += '</ul>';
      }
      return html;
    }
  };

  // ── Generator: template-based content assembly ─────────────────────────────
  var Generator = {
    pick: function (arr) {
      return arr[Math.floor(Math.random() * arr.length)];
    },

    interpolate: function (template) {
      return template.replace(/\{(\w+)\}/g, function (match, key) {
        var vals = BOT_DATA.templateValues[key];
        return vals ? Generator.pick(vals) : match;
      });
    },

    generate: function (type, topic, principal) {
      var tpl = BOT_DATA.templates[type] || BOT_DATA.templates.blog_post;
      var opening = Generator.interpolate(Generator.pick(tpl.openings));
      var body = Generator.interpolate(Generator.pick(tpl.bodies));
      var closing = Generator.interpolate(Generator.pick(tpl.closings));

      var title = topic || 'Untitled Content';
      var fullBody = opening + body + closing;

      return { title: title, body: fullBody, type: type, principal: principal };
    }
  };

  // ── Nav: view switching, toast notifications ───────────────────────────────
  var Nav = {
    switchView: function (viewName) {
      document.querySelectorAll('.bot-view').forEach(function (v) { v.classList.remove('active'); });
      document.querySelectorAll('.bot-nav-link').forEach(function (l) { l.classList.remove('active'); });
      var view = document.getElementById('view-' + viewName);
      if (view) view.classList.add('active');
      var tab = document.querySelector('.bot-nav-link[data-view="' + viewName + '"]');
      if (tab) tab.classList.add('active');

      // Render view
      if (viewName === 'dashboard') Views.renderDashboard();
      if (viewName === 'calendar') Views.renderCalendar();
      if (viewName === 'generate') Views.renderGenerate();
      if (viewName === 'review') Views.renderReview();
    },

    toast: function (message) {
      var el = document.getElementById('bot-toast');
      el.textContent = message;
      el.classList.add('show');
      setTimeout(function () { el.classList.remove('show'); }, 3000);
    }
  };

  // ── Helpers ────────────────────────────────────────────────────────────────
  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function formatDate(dateStr) {
    if (!dateStr) return '\u2014';
    var d = new Date(dateStr + 'T00:00:00');
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  function statusBadge(status) {
    return '<span class="bot-badge bot-badge-' + status + '">' + status + '</span>';
  }

  function typeLabel(type) {
    var map = { blog_post: 'Blog Post', linkedin_post: 'LinkedIn Post', market_report: 'Market Report' };
    return map[type] || type;
  }

  // ── Views ──────────────────────────────────────────────────────────────────
  var Views = {
    renderDashboard: function () {
      var content = Store.getContent();
      var calendar = Store.getCalendar();

      var pending = content.filter(function (c) { return c.status === 'queued' || c.status === 'draft'; }).length;
      var published = content.filter(function (c) { return c.status === 'published'; }).length;
      var today = new Date().toISOString().slice(0, 10);
      var upcoming = calendar.filter(function (c) { return c.date >= today; }).length;

      document.getElementById('dash-stats').innerHTML =
        '<div class="bot-stat-card"><span class="stat-value">' + pending + '</span><span class="stat-label">Pending Review</span></div>' +
        '<div class="bot-stat-card"><span class="stat-value">' + published + '</span><span class="stat-label">Published</span></div>' +
        '<div class="bot-stat-card"><span class="stat-value">' + upcoming + '</span><span class="stat-label">Upcoming</span></div>' +
        '<div class="bot-stat-card"><span class="stat-value">' + content.length + '</span><span class="stat-label">Total Content</span></div>';

      // Recent activity — last 5 content items by date
      var sorted = content.slice().sort(function (a, b) { return (b.created || '').localeCompare(a.created || ''); });
      var actHtml = '';
      sorted.slice(0, 6).forEach(function (c) {
        actHtml += '<li><span>' + escapeHtml(c.title.substring(0, 50)) + (c.title.length > 50 ? '...' : '') + '</span>' + statusBadge(c.status) + '</li>';
      });
      document.getElementById('dash-activity').innerHTML = actHtml || '<li>No content yet.</li>';

      // Upcoming calendar — next 5 entries
      var calSorted = calendar.slice().sort(function (a, b) { return a.date.localeCompare(b.date); });
      var futureEntries = calSorted.filter(function (c) { return c.date >= today; }).slice(0, 5);
      var calHtml = '';
      futureEntries.forEach(function (c) {
        calHtml += '<tr><td>' + formatDate(c.date) + '</td><td>' + escapeHtml(c.topic.substring(0, 40)) + '</td><td>' + typeLabel(c.type) + '</td></tr>';
      });
      document.querySelector('#dash-calendar tbody').innerHTML = calHtml || '<tr><td colspan="3">No upcoming entries.</td></tr>';
    },

    renderCalendar: function () {
      var items = Store.getCalendar().slice().sort(function (a, b) { return a.date.localeCompare(b.date); });
      var html = '';
      items.forEach(function (entry) {
        html += '<tr>' +
          '<td>' + formatDate(entry.date) + '</td>' +
          '<td>' + typeLabel(entry.type) + '</td>' +
          '<td>' + escapeHtml(entry.topic) + '</td>' +
          '<td>' + entry.principal + '</td>' +
          '<td>' + statusBadge(entry.status) + '</td>' +
          '<td><div class="bot-btn-group">' +
            '<button class="bot-btn bot-btn-sm bot-btn-outline" data-action="edit-cal" data-id="' + entry.id + '">Edit</button>' +
            '<button class="bot-btn bot-btn-sm bot-btn-danger" data-action="delete-cal" data-id="' + entry.id + '">Delete</button>' +
            '<button class="bot-btn bot-btn-sm bot-btn-primary" data-action="generate-from-cal" data-id="' + entry.id + '">Generate</button>' +
          '</div></td>' +
          '</tr>';
      });
      document.querySelector('#calendar-table tbody').innerHTML = html || '<tr><td colspan="6">No calendar entries.</td></tr>';
    },

    renderGenerate: function () {
      document.getElementById('generate-form-card').style.display = 'block';
      document.getElementById('generate-loading').style.display = 'none';
      document.getElementById('generate-result').style.display = 'none';
    },

    renderReview: function () {
      var content = Store.getContent().filter(function (c) {
        return c.status !== 'published';
      });
      // Also show published for reference
      var published = Store.getContent().filter(function (c) { return c.status === 'published'; });
      var all = content.concat(published);
      // Sort: queued/draft first, then approved, then published
      var order = { draft: 0, queued: 1, approved: 2, rejected: 3, published: 4 };
      all.sort(function (a, b) { return (order[a.status] || 5) - (order[b.status] || 5); });

      var html = '';
      all.forEach(function (item) {
        html += '<tr class="clickable" data-action="view-detail" data-id="' + item.id + '">' +
          '<td>' + escapeHtml(item.title.substring(0, 50)) + (item.title.length > 50 ? '...' : '') + '</td>' +
          '<td>' + typeLabel(item.type) + '</td>' +
          '<td>' + (item.platform || '\u2014') + '</td>' +
          '<td>' + statusBadge(item.status) + '</td>' +
          '<td>' + Compliance.renderBadge(item.body) + '</td>' +
          '<td>' + item.principal + '</td>' +
          '<td>' + formatDate(item.created) + '</td>' +
          '</tr>';
      });
      document.querySelector('#review-table tbody').innerHTML = html || '<tr><td colspan="7">No content items.</td></tr>';
    },

    renderContentDetail: function (id) {
      var item = Store.getContentById(id);
      if (!item) return;

      Nav.switchView('detail');
      // Remove active from all nav tabs since detail is not a nav item
      document.querySelectorAll('.bot-nav-link').forEach(function (l) { l.classList.remove('active'); });
      document.querySelector('.bot-nav-link[data-view="review"]').classList.add('active');

      document.getElementById('detail-title').textContent = item.title;
      document.getElementById('detail-body').textContent = item.body;

      // Metadata
      var metaHtml =
        '<li><span class="meta-label">Type</span><span>' + typeLabel(item.type) + '</span></li>' +
        '<li><span class="meta-label">Platform</span><span>' + (item.platform || '\u2014') + '</span></li>' +
        '<li><span class="meta-label">Status</span><span>' + statusBadge(item.status) + '</span></li>' +
        '<li><span class="meta-label">Author</span><span>' + item.principal + '</span></li>' +
        '<li><span class="meta-label">Created</span><span>' + formatDate(item.created) + '</span></li>' +
        '<li><span class="meta-label">Published</span><span>' + formatDate(item.published) + '</span></li>';
      if (item.metrics) {
        metaHtml +=
          '<li><span class="meta-label">Views</span><span>' + (item.metrics.views || 0) + '</span></li>' +
          '<li><span class="meta-label">Shares</span><span>' + (item.metrics.shares || 0) + '</span></li>' +
          '<li><span class="meta-label">Engagement</span><span>' + (item.metrics.engagement || '\u2014') + '</span></li>';
      }
      document.getElementById('detail-meta').innerHTML = metaHtml;

      // Compliance
      document.getElementById('detail-compliance').innerHTML = Compliance.renderDetail(item.body);

      // Actions based on status
      var actHtml = '';
      if (item.status === 'draft' || item.status === 'queued') {
        actHtml += '<button class="bot-btn bot-btn-primary" data-action="approve" data-id="' + id + '">Approve</button>';
        actHtml += '<button class="bot-btn bot-btn-danger" data-action="reject" data-id="' + id + '">Reject</button>';
        actHtml += '<button class="bot-btn bot-btn-outline" data-action="edit-content" data-id="' + id + '">Edit</button>';
      } else if (item.status === 'approved') {
        actHtml += '<button class="bot-btn bot-btn-primary" data-action="publish" data-id="' + id + '">Publish</button>';
        actHtml += '<button class="bot-btn bot-btn-outline" data-action="edit-content" data-id="' + id + '">Edit</button>';
      } else if (item.status === 'rejected') {
        actHtml += '<button class="bot-btn bot-btn-outline" data-action="edit-content" data-id="' + id + '">Edit & Resubmit</button>';
      }
      actHtml += '<button class="bot-btn bot-btn-danger" data-action="delete-content" data-id="' + id + '" style="margin-top:8px;">Delete</button>';
      document.getElementById('detail-actions').innerHTML = actHtml;
    }
  };

  // ── Temporary state for generated content ──────────────────────────────────
  var generatedContent = null;

  // ── Event Handlers ─────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    Store.init();

    // Nav tab clicks
    document.querySelectorAll('.bot-nav-link[data-view]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        Nav.switchView(this.dataset.view);
      });
    });

    // Calendar form submit
    document.getElementById('calendar-form').addEventListener('submit', function (e) {
      e.preventDefault();
      Store.addCalendarEntry({
        date: document.getElementById('cal-date').value,
        type: document.getElementById('cal-type').value,
        topic: document.getElementById('cal-topic').value,
        principal: document.getElementById('cal-principal').value,
        notes: document.getElementById('cal-notes').value
      });
      this.reset();
      Views.renderCalendar();
      Nav.toast('Calendar entry added');
    });

    // Calendar table actions (delegated)
    document.getElementById('calendar-table').addEventListener('click', function (e) {
      var btn = e.target.closest('[data-action]');
      if (!btn) return;
      var action = btn.dataset.action;
      var id = btn.dataset.id;

      if (action === 'delete-cal') {
        Store.deleteCalendarEntry(id);
        Views.renderCalendar();
        Nav.toast('Entry deleted');
      }

      if (action === 'edit-cal') {
        var entry = Store.getCalendar().find(function (c) { return c.id === id; });
        if (!entry) return;
        document.getElementById('edit-cal-id').value = entry.id;
        document.getElementById('edit-cal-date').value = entry.date;
        document.getElementById('edit-cal-type').value = entry.type;
        document.getElementById('edit-cal-topic').value = entry.topic;
        document.getElementById('edit-cal-principal').value = entry.principal;
        document.getElementById('edit-cal-notes').value = entry.notes || '';
        document.getElementById('modal-edit-calendar').classList.add('active');
      }

      if (action === 'generate-from-cal') {
        var calEntry = Store.getCalendar().find(function (c) { return c.id === id; });
        if (!calEntry) return;
        Nav.switchView('generate');
        document.getElementById('gen-type').value = calEntry.type;
        document.getElementById('gen-topic').value = calEntry.topic;
        document.getElementById('gen-principal').value = calEntry.principal;
        if (calEntry.type === 'linkedin_post') {
          document.getElementById('gen-platform').value = 'linkedin';
        } else {
          document.getElementById('gen-platform').value = 'website';
        }
      }
    });

    // Edit calendar modal
    document.getElementById('btn-cancel-edit').addEventListener('click', function () {
      document.getElementById('modal-edit-calendar').classList.remove('active');
    });

    document.getElementById('edit-calendar-form').addEventListener('submit', function (e) {
      e.preventDefault();
      Store.updateCalendarEntry(document.getElementById('edit-cal-id').value, {
        date: document.getElementById('edit-cal-date').value,
        type: document.getElementById('edit-cal-type').value,
        topic: document.getElementById('edit-cal-topic').value,
        principal: document.getElementById('edit-cal-principal').value,
        notes: document.getElementById('edit-cal-notes').value
      });
      document.getElementById('modal-edit-calendar').classList.remove('active');
      Views.renderCalendar();
      Nav.toast('Entry updated');
    });

    // Close modal on overlay click
    document.querySelectorAll('.bot-modal-overlay').forEach(function (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) overlay.classList.remove('active');
      });
    });

    // Generate form submit
    document.getElementById('generate-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var type = document.getElementById('gen-type').value;
      var topic = document.getElementById('gen-topic').value;
      var principal = document.getElementById('gen-principal').value;
      var platform = document.getElementById('gen-platform').value;

      document.getElementById('generate-form-card').style.display = 'none';
      document.getElementById('generate-loading').style.display = 'block';
      document.getElementById('generate-result').style.display = 'none';

      // Simulated 2.5s delay
      setTimeout(function () {
        generatedContent = Generator.generate(type, topic, principal);
        generatedContent.platform = platform;
        generatedContent.status = 'draft';

        document.getElementById('generate-loading').style.display = 'none';
        document.getElementById('generate-result').style.display = 'block';

        document.getElementById('generate-result-meta').innerHTML =
          '<p style="font-size:14px;color:var(--muted);">' +
          typeLabel(type) + ' &middot; ' + platform + ' &middot; ' + principal +
          '</p>';
        document.getElementById('generate-result-body').textContent = generatedContent.body;
        document.getElementById('generate-result-compliance').innerHTML = Compliance.renderDetail(generatedContent.body);
      }, 2500);
    });

    // Send to queue
    document.getElementById('btn-send-to-queue').addEventListener('click', function () {
      if (!generatedContent) return;
      generatedContent.status = 'queued';
      Store.addContent(generatedContent);
      generatedContent = null;
      Nav.toast('Content sent to review queue');
      Nav.switchView('review');
    });

    // Regenerate
    document.getElementById('btn-regenerate').addEventListener('click', function () {
      document.getElementById('generate-result').style.display = 'none';
      document.getElementById('generate-form-card').style.display = 'block';
    });

    // Review table click (delegated)
    document.getElementById('review-table').addEventListener('click', function (e) {
      var row = e.target.closest('tr[data-action="view-detail"]');
      if (row) {
        Views.renderContentDetail(row.dataset.id);
      }
    });

    // Back to review
    document.getElementById('btn-back-to-review').addEventListener('click', function () {
      Nav.switchView('review');
    });

    // Content detail actions (delegated)
    document.getElementById('detail-actions').addEventListener('click', function (e) {
      var btn = e.target.closest('[data-action]');
      if (!btn) return;
      var action = btn.dataset.action;
      var id = btn.dataset.id;

      if (action === 'approve') {
        Store.updateContent(id, { status: 'approved' });
        Views.renderContentDetail(id);
        Nav.toast('Content approved');
      }

      if (action === 'reject') {
        Store.updateContent(id, { status: 'rejected' });
        Views.renderContentDetail(id);
        Nav.toast('Content rejected');
      }

      if (action === 'publish') {
        Store.updateContent(id, { status: 'published', published: new Date().toISOString().slice(0, 10) });
        Views.renderContentDetail(id);
        Nav.toast('Content published');
      }

      if (action === 'delete-content') {
        var items = Store.getContent().filter(function (c) { return c.id !== id; });
        Store.saveContent(items);
        Nav.toast('Content deleted');
        Nav.switchView('review');
      }

      if (action === 'edit-content') {
        var item = Store.getContentById(id);
        if (!item) return;
        document.getElementById('edit-content-id').value = item.id;
        document.getElementById('edit-content-title').value = item.title;
        document.getElementById('edit-content-body').value = item.body;
        document.getElementById('modal-edit-content').classList.add('active');
      }
    });

    // Edit content modal
    document.getElementById('btn-cancel-edit-content').addEventListener('click', function () {
      document.getElementById('modal-edit-content').classList.remove('active');
    });

    document.getElementById('edit-content-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var id = document.getElementById('edit-content-id').value;
      var updates = {
        title: document.getElementById('edit-content-title').value,
        body: document.getElementById('edit-content-body').value
      };
      // If rejected, move back to queued on edit
      var item = Store.getContentById(id);
      if (item && item.status === 'rejected') {
        updates.status = 'queued';
      }
      Store.updateContent(id, updates);
      document.getElementById('modal-edit-content').classList.remove('active');
      Views.renderContentDetail(id);
      Nav.toast('Content updated');
    });

    // Initial render
    Views.renderDashboard();
  });
})();
