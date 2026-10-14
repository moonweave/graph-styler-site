import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const root = new URL('../', import.meta.url);
const html = fs.readFileSync(new URL('index.html', root), 'utf8');
const elements = [...html.matchAll(/<(?:img|a)\b[^>]*data-en-(?:src|href)=[^>]*>/g)].map(([tag]) => {
  const attrs = Object.fromEntries([...tag.matchAll(/([\w-]+)="([^"]*)"/g)].map(([, key, value]) => [key, value]));
  return { attrs, getAttribute: (key) => attrs[key], setAttribute: (key, value) => { attrs[key] = value; } };
});
assert.equal(elements.length, 8);
const buttons = ['ko', 'en'].map((lang) => ({
  dataset: { lang }, classList: { toggle() {} },
  addEventListener(_, callback) { this.click = callback; },
}));
const document = {
  documentElement: { lang: 'ko' },
  querySelector() { return null; },
  querySelectorAll(selector) {
    if (selector === '.lang-btn') return buttons;
    const attr = selector.match(/^\[([^\]]+)\]$/)?.[1];
    return attr ? elements.filter((element) => attr in element.attrs) : [];
  },
};
vm.runInNewContext(fs.readFileSync(new URL('script.js', root), 'utf8'), {
  document, URLSearchParams, window: { location: { pathname: '/', search: '' } },
  localStorage: { getItem() { return null; }, setItem() {} },
});
for (const lang of ['en', 'ko', 'en']) {
  buttons.find((button) => button.dataset.lang === lang).click();
  assert.equal(document.documentElement.lang, lang);
  for (const element of elements) {
    for (const attr of ['src', 'href', 'height']) {
      if (`data-${lang}-${attr}` in element.attrs) {
        assert.equal(element.attrs[attr], element.attrs[`data-${lang}-${attr}`]);
      }
    }
  }
}
console.log('Language switch updates screenshot sources, full-size links and dimensions');
