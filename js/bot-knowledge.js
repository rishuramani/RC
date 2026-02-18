/**
 * RC Marketing Bot - Knowledge Base Tab Switching & Rendering
 */
document.addEventListener('DOMContentLoaded', function () {
  // Tab switching
  document.querySelectorAll('.bot-kb-tab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      document.querySelectorAll('.bot-kb-tab').forEach(function (t) { t.classList.remove('active'); });
      document.querySelectorAll('.bot-kb-panel').forEach(function (p) { p.classList.remove('active'); });
      tab.classList.add('active');
      document.getElementById('panel-' + tab.dataset.tab).classList.add('active');
    });
  });

  renderFirmFacts();
  renderMarketData();
  renderDataSources();
  renderBrandRules();
});

function renderFirmFacts() {
  var container = document.getElementById('kb-firm-facts');
  var categories = BOT_DATA.firmFacts;
  var html = '';
  var labels = { track_record: 'Track Record', portfolio: 'Portfolio', thesis: 'Investment Thesis', advantage: 'Competitive Advantages', terms: 'Terms & Fees' };

  Object.keys(categories).forEach(function (cat) {
    html += '<div class="bot-card"><h3>' + labels[cat] + '</h3><table class="bot-table"><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>';
    categories[cat].forEach(function (item) {
      html += '<tr><td>' + item.label + '</td><td><strong>' + item.value + '</strong></td></tr>';
    });
    html += '</tbody></table></div>';
  });
  container.innerHTML = html;
}

function renderMarketData() {
  var container = document.getElementById('kb-market-data');
  var data = BOT_DATA.marketData;
  var html = '';

  Object.keys(data).forEach(function (market) {
    Object.keys(data[market]).forEach(function (period) {
      html += '<div class="bot-card"><h3>' + market.charAt(0).toUpperCase() + market.slice(1) + ' \u2014 ' + period + '</h3><table class="bot-table"><thead><tr><th>Metric</th><th>Value</th><th>Source</th></tr></thead><tbody>';
      data[market][period].forEach(function (item) {
        html += '<tr><td>' + item.metric + '</td><td><strong>' + item.value + '</strong></td><td>' + item.source + '</td></tr>';
      });
      html += '</tbody></table></div>';
    });
  });
  container.innerHTML = html;
}

function renderDataSources() {
  var container = document.getElementById('kb-data-sources');
  var html = '<div class="bot-card"><h3>Data Sources</h3><table class="bot-table"><thead><tr><th>Source</th><th>Frequency</th><th>Notes</th><th>URL</th></tr></thead><tbody>';
  BOT_DATA.dataSources.forEach(function (src) {
    var urlCell = src.url ? '<a href="' + src.url + '" target="_blank" rel="noopener">' + src.url + '</a>' : 'Subscription';
    html += '<tr><td><strong>' + src.name + '</strong></td><td>' + src.frequency + '</td><td>' + src.notes + '</td><td>' + urlCell + '</td></tr>';
  });
  html += '</tbody></table></div>';
  container.innerHTML = html;
}

function renderBrandRules() {
  var container = document.getElementById('kb-brand-rules');
  var rules = BOT_DATA.brandRules;
  var labels = { terminology: 'Terminology', tone: 'Tone & Style', compliance: 'Compliance', avoid: 'Terms to Avoid' };
  var html = '';

  Object.keys(rules).forEach(function (type) {
    html += '<div class="bot-card"><h3>' + labels[type] + '</h3><table class="bot-table"><thead><tr><th>Rule</th>';
    if (type !== 'avoid') html += '<th>Example</th>';
    html += '</tr></thead><tbody>';
    rules[type].forEach(function (item) {
      html += '<tr><td>' + item.rule + '</td>';
      if (type !== 'avoid') html += '<td>' + (item.example || '\u2014') + '</td>';
      html += '</tr>';
    });
    html += '</tbody></table></div>';
  });
  container.innerHTML = html;
}
