# -*- coding: utf-8 -*-
"""对已部署的高性价比人生指南站点做三类改动：
1) 去掉广告、赞赏码、原作者 GA 统计；
2) 站内 GitHub 导航链接改指自己的 fork，域名元数据改指自己的域名；
3) README.md 尾部推广段落（Star 走势 / 赞赏 / 广告位 / 商务合作）删除；
4) 导航栏与侧栏增加指向《人情世故指南》的双向友链。
每个替换都断言命中次数，全部通过才落盘。用法：python patch_site.py <站点根目录>
"""
import sys, os

root = sys.argv[1] if len(sys.argv) > 1 else '.'
FORK = 'https://github.com/xiaobai5211314/HowToLiveBetter'
ORIG = 'https://github.com/eternity4719/HowToLiveBetter'
SITE = 'https://rensheng.21212121.xyz'

def cut(s, start, end):
    """删除 start（含）到 end（含）之间的片段。"""
    if start not in s:
        return s
    i = s.index(start)
    if end not in s[i:]:
        return s
    j = s.index(end, i) + len(end)
    return s[:i] + s[j:]

def rep(s, old, new, expect=1):
    n = s.count(old)
    if n == 0 and new in s:
        return s
    if n != expect and new in s:
        return s
    assert n == expect, 'expected %d, found %d: %r' % (expect, n, old[:70])
    return s.replace(old, new)

def load(name):
    with open(os.path.join(root, name), encoding='utf-8') as f:
        return f.read()

out = {}

# ---------------- index.html ----------------
s = load('index.html')

# 1) GA 统计脚本：保留离线构建的剥离标记（tools/offline/build.mjs 依赖），去掉脚本本体
if '<!-- ga:start' in s and '<!-- ga:end -->' in s:
    i = s.index('<!-- ga:start')
    j = s.index('\n', i) + 1
    k = s.index('<!-- ga:end -->')
    if j < k:
        between = s[j:k].strip()
        if between:
            s = s[:j] + s[k:]

# 2) 广告/赞赏 CSS（含两条注释）
s = cut(s, '/* 侧栏底部广告位', '#tip-box button:hover{color:var(--t1);background:var(--bg-mute)}\n')

# 3) 侧栏广告块 + 「请作者喝杯咖啡」按钮
s = cut(s, '  <div class="group ad">',
        '    <button type="button" class="tip-open" id="tip-open">觉得有用？请作者喝杯咖啡</button>\n  </div>\n')

# 4) 微信赞赏码弹窗
s = cut(s, '<div id="tip-mask" hidden>',
        '    <button type="button" id="tip-x">关闭</button>\n  </div>\n</div>\n')

# 5) 赞赏码 JS
s = cut(s, '/* ---------- 赞赏码弹窗 ---------- */',
        "document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && !TIP.hidden){ ev.stopPropagation(); tipClose(); } }, true);\n")

# 6) GA 的 track/reportSearch 函数及搜索上报调用
s = cut(s, '// 离线单文件会把 GA 片段整段剥掉',
        "  track('search', { search_term: q, results: Number(document.getElementById('cnt').textContent) || 0 });\n}\n")
s = rep(s, """  // 上报比筛选晚得多：按 120ms 那一拍发，「高血压」会被当成「高」「高血」「高血压」三次搜索
  let tm, qtm; document.getElementById('q').addEventListener('input', e => {
    clearTimeout(tm); tm = setTimeout(() => { state.q = e.target.value.trim(); apply(); }, 120);
    clearTimeout(qtm); qtm = setTimeout(reportSearch, 2000);
  });""",
"""  let tm; document.getElementById('q').addEventListener('input', e => {
    clearTimeout(tm); tm = setTimeout(() => { state.q = e.target.value.trim(); apply(); }, 120);
  });""")
s = rep(s, "  if (window.gtag) gtag('event', 'doc_open', { doc: path });\n", '')

# 7) book/ 目录链接改指自己 fork 的目录树（本站没有目录索引页）
s = rep(s, 'href="book/"', 'href="%s/tree/main/book"' % FORK, expect=2)

# 8) 元数据域名改指自己站点；GitHub 链接改指自己的 fork
s = rep(s, 'https://eternity4719.github.io/HowToLiveBetter', SITE, expect=9)
s = rep(s, ORIG, FORK, expect=15)

# 9) 页脚：CC BY 4.0 要求保留原作署名与原文链接
s = rep(s,
        '正文按 <a href="https://creativecommons.org/licenses/by/4.0/deed.zh-hans">CC BY 4.0</a> 发布，转载改编请署名并附原文链接。',
        '正文原作《高性价比人生指南》（原作者 <a href="%s">eternity4719</a>），按 <a href="https://creativecommons.org/licenses/by/4.0/deed.zh-hans">CC BY 4.0</a> 授权；本站在原作基础上删改。' % ORIG)

# 10) 友链：导航栏与侧栏互指《人情世故指南》
if '.special-link' not in s:
    s = rep(s,
            '.nav-r{display:flex;align-items:center;gap:8px}',
            '.nav-r{display:flex;align-items:center;gap:8px}\n'
            '.special-link{display:inline-flex;align-items:center;color:var(--brand-1);font-weight:600;font-size:13.5px;text-decoration:none;padding:5px 9px;border-radius:6px;transition:all .2s;white-space:nowrap;margin-right:2px}\n'
            '.special-link:hover{background:var(--bg-mute);color:var(--brand-2);text-decoration:none}\n'
            '@media (max-width:640px){.special-link{display:none}}')

    s = rep(s,
            '    <div class="nav-r">\n      <a class="icon-btn" href="README.md"',
            '    <div class="nav-r">\n      <a class="special-link" href="https://renqing.21212121.xyz/" target="_blank" rel="noopener" title="访问《人情世故指南》">人情世故 ↗</a>\n      <a class="icon-btn" href="README.md"')

    s = rep(s,
            '    <p>正文与标签来自仓库 <a href="%s/tree/main/book">book/</a> 下的 34 个文件，改正文即改这里。</p>\n  </div>' % FORK,
            '    <p>正文与标签来自仓库 <a href="%s/tree/main/book">book/</a> 下的 34 个文件，改正文即改这里。</p>\n    <p style="margin-top:10px;padding-top:8px;border-top:1px dashed var(--divider)">🤝 <b>友链：</b><a href="https://renqing.21212121.xyz/" target="_blank" rel="noopener">人情世故指南 ↗</a></p>\n  </div>' % FORK)

assert 'mcyyy' not in s and 'gtag' not in s and 'googletagmanager' not in s
assert 'eternity4719.github.io' not in s and 'tip-mask' not in s and 'reportSearch' not in s
assert 'renqing.21212121.xyz' in s
out['index.html'] = s

# ---------------- README.md ----------------
s = load('README.md')

# 尾部推广段整体删除：## Star 走势 / ## 赞赏 / ## 广告位 / ## 商务合作
if '\n## Star 走势' in s:
    idx = s.index('\n## Star 走势')
    s = s[:idx] + '\n'

# 许可段的原文链接按 CC BY 协议保留指向原作；其余仓库链接（含 release 下载）指向自己的 fork
s = rep(s, '附上仓库链接 ' + ORIG + ' 。', '附上仓库链接 __ATTRURL__ 。', expect=1)
s = rep(s, 'https://eternity4719.github.io/HowToLiveBetter', SITE, expect=6)
s = rep(s, ORIG, FORK, expect=11)         # 提 issue + release 下载 + 正文复述下载 + git clone
s = rep(s, '__ATTRURL__', ORIG, expect=1)
assert 'mcyyy' not in s and 'star-history' not in s and '赞赏' not in s
out['README.md'] = s

# ---------------- selfcheck.html（生活自查页）----------------
s = load('selfcheck.html')
s = s.replace('https://eternity4719.github.io/HowToLiveBetter', SITE)
s = s.replace(ORIG, FORK)
assert 'mcyyy' not in s and 'gtag' not in s and 'googletagmanager' not in s
assert 'eternity4719' not in s and 'tip-mask' not in s and '赞赏' not in s
out['selfcheck.html'] = s

# ---------------- sitemap.xml / robots.txt ----------------
for name, n in (('sitemap.xml', 3), ('robots.txt', 1)):
    s = load(name)
    s = rep(s, 'https://eternity4719.github.io/HowToLiveBetter', SITE, expect=n)
    out[name] = s

for name, s in out.items():
    with open(os.path.join(root, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)
    print('patched', name)
print('ALL OK')
