# -*- coding: utf-8 -*-
"""把站点 UI 换成 Claude Code 官网的设计语言（暖羊皮纸 + 衬线标题 + 陶土橙）。
只改样式令牌与少量组件样式，不动结构与 JS。断言式替换：全部命中才落盘。
用法：python restyle_site.py <站点根目录>   目标文件 index.html
"""
import sys, os

root = sys.argv[1] if len(sys.argv) > 1 else '.'
path = os.path.join(root, 'index.html')
with open(path, encoding='utf-8') as f:
    s = f.read()

def rep(s, old, new, expect=1):
    n = s.count(old)
    if n == 0 and new in s:
        return s
    assert n == expect, 'expected %d, found %d: %r' % (expect, n, old[:70])
    return s.replace(old, new)

# 1) 字体：加 Noto Serif SC（标题衬线）
s = rep(s, 'family=Inter:wght@400;500;600;700&display=swap',
        'family=Inter:wght@400;500;600;700&family=Noto+Serif+SC:wght@500;600&display=swap')

# 2) 浅色令牌：白/冷灰/蓝 -> 羊皮纸/暖灰/陶土橙
s = rep(s, """  --bg:#ffffff; --bg-alt:#f6f6f7; --bg-soft:#f6f6f7; --bg-mute:#f1f1f2; --bg-elv:#ffffff;
  --divider:#e2e2e3; --gutter:#e2e2e3;
  --t1:rgba(60,60,67,1); --t2:rgba(60,60,67,.78); --t3:rgba(60,60,67,.56);
  --brand-1:#3451b2; --brand-2:#3a5ccc; --brand-3:#5672cd; --brand-soft:rgba(100,108,255,.14);
  --green-1:#18794e; --green-soft:rgba(16,185,129,.14);
  --yellow-1:#915930; --yellow-soft:rgba(234,179,8,.14);
  --red-1:#b8272c; --red-soft:rgba(244,63,94,.14);
  --gray-1:#565a5f; --gray-soft:rgba(142,150,170,.14);
  --mark:rgba(234,179,8,.32);
  --shadow:0 1px 2px rgba(0,0,0,.04),0 1px 2px rgba(0,0,0,.06);""",
"""  --bg:#f5f4ed; --bg-alt:#edebe1; --bg-soft:#faf9f5; --bg-mute:#e8e6dc; --bg-elv:#faf9f5;
  --divider:#e0ddcf; --gutter:#e8e6dc;
  --t1:#141413; --t2:#5e5d59; --t3:#87867f;
  --brand-1:#c96442; --brand-2:#b4573a; --brand-3:#d97757; --brand-soft:rgba(201,100,66,.11);
  --green-1:#4d7c5f; --green-soft:rgba(77,124,95,.13);
  --yellow-1:#96602e; --yellow-soft:rgba(201,140,80,.15);
  --red-1:#b53333; --red-soft:rgba(181,51,51,.10);
  --gray-1:#5e5d59; --gray-soft:rgba(139,134,120,.13);
  --mark:rgba(217,119,87,.28);
  --shadow:0 1px 2px rgba(40,35,25,.05),0 4px 24px rgba(40,35,25,.06);""")

# 3) 加衬线字体变量
if '--font-serif:' not in s:
    s = rep(s, '  --mono:ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;',
            '  --font-serif:"Noto Serif SC","Source Han Serif SC","Songti SC",Georgia,"Times New Roman",serif;\n  --mono:ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;')

# 4) 深色令牌：冷黑 -> 暖黑
s = rep(s, """  --bg:#1b1b1f; --bg-alt:#161618; --bg-soft:#202127; --bg-mute:#2b2b2f; --bg-elv:#202127;
  --divider:#2e2e32; --gutter:#000000;
  --t1:rgba(255,255,245,.86); --t2:rgba(235,235,245,.6); --t3:rgba(235,235,245,.38);
  --brand-1:#a8b1ff; --brand-2:#5c73e7; --brand-3:#3e63dd; --brand-soft:rgba(100,108,255,.16);
  --green-1:#3dd68c; --green-soft:rgba(16,185,129,.16);
  --yellow-1:#f9b44e; --yellow-soft:rgba(234,179,8,.16);
  --red-1:#f66f81; --red-soft:rgba(244,63,94,.16);
  --gray-1:#a4a8ae; --gray-soft:rgba(142,150,170,.16);
  --mark:rgba(234,179,8,.28);
  --shadow:0 1px 2px rgba(0,0,0,.3);""",
"""  --bg:#141413; --bg-alt:#1a1a17; --bg-soft:#1f1f1b; --bg-mute:#2b2b27; --bg-elv:#232320;
  --divider:#30302e; --gutter:#000000;
  --t1:#faf9f5; --t2:#b0aea5; --t3:#87867f;
  --brand-1:#d97757; --brand-2:#e08a6d; --brand-3:#c96442; --brand-soft:rgba(217,119,87,.16);
  --green-1:#8fbf9d; --green-soft:rgba(143,191,157,.14);
  --yellow-1:#d9a066; --yellow-soft:rgba(217,160,102,.15);
  --red-1:#e0837c; --red-soft:rgba(224,131,124,.14);
  --gray-1:#a09c90; --gray-soft:rgba(160,156,144,.14);
  --mark:rgba(217,119,87,.30);
  --shadow:0 1px 2px rgba(0,0,0,.35);""")

# 5) 选区配色
s = rep(s, ':focus-visible{outline:2px solid var(--brand-1);outline-offset:2px;border-radius:4px}\nmark{',
        ':focus-visible{outline:2px solid var(--brand-1);outline-offset:2px;border-radius:4px}\n::selection{background:var(--mark)}\nmark{')

# 6) 字标衬线 + logo 纯色陶土
s = rep(s, '.title{display:flex;align-items:center;gap:10px;font-weight:600;font-size:16px;color:var(--t1);white-space:nowrap}',
        '.title{display:flex;align-items:center;gap:10px;font-family:var(--font-serif);font-weight:600;font-size:17px;color:var(--t1);white-space:nowrap}')
s = rep(s, '.logo{width:24px;height:24px;border-radius:6px;background:linear-gradient(135deg,var(--brand-3),var(--brand-1));display:grid;place-items:center;color:#fff;font-size:12px;font-weight:700}',
        '.logo{width:24px;height:24px;border-radius:8px;background:var(--brand-1);display:grid;place-items:center;color:#faf9f5;font-size:12px;font-weight:700}')

# 7) 搜索框：暖沙底 + 聚焦光环
s = rep(s, """.search input{width:100%;height:40px;padding:0 44px 0 40px;border-radius:8px;border:1px solid transparent;background:var(--bg-alt);color:var(--t1);font:inherit;font-size:14px;transition:border-color .25s,background .25s}
.search input:hover{border-color:var(--divider)}
.search input:focus{outline:0;border-color:var(--brand-1);background:var(--bg)}""",
""".search input{width:100%;height:40px;padding:0 44px 0 40px;border-radius:10px;border:1px solid transparent;background:var(--bg-mute);color:var(--t1);font:inherit;font-size:14px;transition:border-color .25s,background .25s,box-shadow .25s}
.search input:hover{border-color:var(--divider)}
.search input:focus{outline:0;border-color:var(--brand-3);background:var(--bg-elv);box-shadow:0 0 0 3px var(--brand-soft)}""")

# 8) 标题衬线化
s = rep(s, '.doc-head h1{font-size:32px;line-height:40px;font-weight:700;letter-spacing:-.02em;margin:0 0 8px}',
        '.doc-head h1{font-family:var(--font-serif);font-size:33px;line-height:1.32;font-weight:600;letter-spacing:0;margin:0 0 10px}')
s = rep(s, '.sec-h h2{font-size:24px;line-height:32px;font-weight:600;letter-spacing:-.02em;margin:0}',
        '.sec-h h2{font-family:var(--font-serif);font-size:25px;line-height:1.4;font-weight:500;letter-spacing:0;margin:0}')
s = rep(s, '.card-h h3{margin:0;font-size:18px;line-height:28px;font-weight:600;letter-spacing:-.01em;flex:1;min-width:0;overflow-wrap:anywhere}',
        '.card-h h3{margin:0;font-family:var(--font-serif);font-size:18px;line-height:1.55;font-weight:500;letter-spacing:0;flex:1;min-width:0;overflow-wrap:anywhere}')
s = rep(s, '.dm-doc h2{font-size:17px;font-weight:600;margin:26px 0 10px;padding-top:6px;border-top:1px solid var(--divider)}',
        '.dm-doc h2{font-family:var(--font-serif);font-size:19px;font-weight:500;margin:26px 0 10px;padding-top:6px;border-top:1px solid var(--divider)}')

# 9) 卡片：象牙面 + 奶油描边 + 悬停轻影
s = rep(s, """.card{background:var(--bg-soft);border:1px solid transparent;border-radius:12px;padding:22px 24px 18px;margin-bottom:16px;transition:border-color .25s,background .25s;content-visibility:auto;contain-intrinsic-size:300px;contain-intrinsic-size:auto 300px}
.card:hover{border-color:var(--divider)}""",
""".card{background:var(--bg-elv);border:1px solid var(--divider);border-radius:12px;padding:22px 24px 18px;margin-bottom:16px;transition:border-color .25s,box-shadow .25s,background .25s;content-visibility:auto;contain-intrinsic-size:300px;contain-intrinsic-size:auto 300px}
.card:hover{border-color:var(--gutter);box-shadow:var(--shadow)}""")

# 10) 摘要块：左色条改暖沙圆角块
s = rep(s, '.human{margin:0 0 14px;padding:10px 14px;border-left:2px solid var(--brand-1);background:var(--brand-soft);border-radius:0 6px 6px 0;font-size:15px;line-height:1.75;color:var(--t1);overflow-wrap:anywhere}',
        '.human{margin:0 0 14px;padding:12px 16px;background:var(--bg-mute);border-radius:10px;font-size:15px;line-height:1.8;color:var(--t1);overflow-wrap:anywhere}')

# 11) 移动端标题字号
s = rep(s, '  .doc-head h1{font-size:26px;line-height:34px}', '  .doc-head h1{font-size:27px;line-height:1.35}')
s = rep(s, '  .card-h h3{font-size:16px;line-height:24px}', '  .card-h h3{font-size:17px;line-height:1.55}')

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)
print('restyled index.html')

# ---------------- selfcheck.html（生活自查页）----------------
# 与 index.html 同一套设计令牌与组件语言：暖羊皮纸底、陶土橙、衬线标题、
# 象牙卡片 + 奶油描边 + 悬停轻影、暖沙提示块、暖黑深色模式。
sp = os.path.join(root, 'selfcheck.html')
if os.path.exists(sp):
    with open(sp, encoding='utf-8') as f:
        t = f.read()

    # 12) 字体：与 index.html 同一份 Inter + Noto Serif SC
    t = rep(t, '</title>\n<meta name="description"',
            '</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+SC:wght@500;600&display=swap" rel="stylesheet">\n'
            '<meta name="description"')

    # 13) 浅色令牌：白/冷灰/蓝 -> 羊皮纸/暖灰/陶土橙，并补齐卡片用的 --bg-elv/--gutter/--mark/--shadow
    t = rep(t, """  --bg:#ffffff; --bg-alt:#f6f6f7; --bg-soft:#f6f6f7; --bg-mute:#f1f1f2;
  --divider:#e2e2e3;
  --t1:rgba(60,60,67,1); --t2:rgba(60,60,67,.78); --t3:rgba(60,60,67,.56);
  --brand-1:#3451b2; --brand-2:#3a5ccc; --brand-soft:rgba(100,108,255,.14);
  --green-1:#18794e; --green-soft:rgba(16,185,129,.14);
  --yellow-1:#915930; --yellow-soft:rgba(234,179,8,.14);
  --red-1:#b8272c; --red-soft:rgba(244,63,94,.14);
  --gray-1:#565a5f; --gray-soft:rgba(142,150,170,.14);
  --font:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",sans-serif;""",
"""  --bg:#f5f4ed; --bg-alt:#edebe1; --bg-soft:#faf9f5; --bg-mute:#e8e6dc; --bg-elv:#faf9f5;
  --divider:#e0ddcf; --gutter:#e8e6dc;
  --t1:#141413; --t2:#5e5d59; --t3:#87867f;
  --brand-1:#c96442; --brand-2:#b4573a; --brand-3:#d97757; --brand-soft:rgba(201,100,66,.11);
  --green-1:#4d7c5f; --green-soft:rgba(77,124,95,.13);
  --yellow-1:#96602e; --yellow-soft:rgba(201,140,80,.15);
  --red-1:#b53333; --red-soft:rgba(181,51,51,.10);
  --gray-1:#5e5d59; --gray-soft:rgba(139,134,120,.13);
  --mark:rgba(217,119,87,.28);
  --shadow:0 1px 2px rgba(40,35,25,.05),0 4px 24px rgba(40,35,25,.06);
  --font:"Inter",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",sans-serif;
  --font-serif:"Noto Serif SC","Source Han Serif SC","Songti SC",Georgia,"Times New Roman",serif;""")

    # 14) 深色令牌：冷蓝黑 -> 暖黑
    t = rep(t, """  --bg:#1b1b1f; --bg-alt:#161618; --bg-soft:#202127; --bg-mute:#2b2b2f;
  --divider:#2e2e32;
  --t1:rgba(255,255,245,.86); --t2:rgba(235,235,245,.6); --t3:rgba(235,235,245,.38);
  --brand-1:#a8b1ff; --brand-2:#5c73e7; --brand-soft:rgba(100,108,255,.16);
  --green-1:#3dd68c; --green-soft:rgba(16,185,129,.16);
  --yellow-1:#f9b44e; --yellow-soft:rgba(234,179,8,.16);
  --red-1:#f66f81; --red-soft:rgba(244,63,94,.16);
  --gray-1:#a4a8ae; --gray-soft:rgba(142,150,170,.16);""",
"""  --bg:#141413; --bg-alt:#1a1a17; --bg-soft:#1f1f1b; --bg-mute:#2b2b27; --bg-elv:#232320;
  --divider:#30302e; --gutter:#000000;
  --t1:#faf9f5; --t2:#b0aea5; --t3:#87867f;
  --brand-1:#d97757; --brand-2:#e08a6d; --brand-3:#c96442; --brand-soft:rgba(217,119,87,.16);
  --green-1:#8fbf9d; --green-soft:rgba(143,191,157,.14);
  --yellow-1:#d9a066; --yellow-soft:rgba(217,160,102,.15);
  --red-1:#e0837c; --red-soft:rgba(224,131,124,.14);
  --gray-1:#a09c90; --gray-soft:rgba(160,156,144,.14);
  --mark:rgba(217,119,87,.30);
  --shadow:0 1px 2px rgba(0,0,0,.35);""")

    # 15) 标题与字标改衬线
    t = rep(t, 'h1{font-size:28px;line-height:1.3;margin:0 0 12px;font-weight:600;letter-spacing:-.01em}',
            'h1{font-family:var(--font-serif);font-size:33px;line-height:1.32;margin:0 0 12px;font-weight:600;letter-spacing:0}')
    t = rep(t, 'h2{font-size:18px;font-weight:600;margin:36px 0 4px;padding-top:24px;border-top:1px solid var(--divider)}',
            'h2{font-family:var(--font-serif);font-size:19px;font-weight:500;margin:36px 0 4px;padding-top:24px;border-top:1px solid var(--divider)}')
    t = rep(t, '.nav .title{font-weight:600;font-size:16px;color:var(--t1)}',
            '.nav .title{font-family:var(--font-serif);font-weight:600;font-size:17px;color:var(--t1)}')

    # 16) 卡片：象牙面 + 奶油描边 + 悬停轻影
    t = rep(t, '.card{border:1px solid var(--divider);border-radius:12px;padding:16px 20px;margin:12px 0;background:var(--bg)}',
            '.card{border:1px solid var(--divider);border-radius:12px;padding:16px 20px;margin:12px 0;background:var(--bg-elv);transition:border-color .25s,box-shadow .25s,background .25s}\n'
            '.card:hover{border-color:var(--gutter);box-shadow:var(--shadow)}')

    # 17) 提示块改暖沙圆角、汇总数字块改象牙面
    t = rep(t, '.note{font-size:13.5px;color:var(--t2);background:var(--bg-soft);border-radius:8px;padding:12px 16px;margin:20px 0}',
            '.note{font-size:13.5px;color:var(--t2);background:var(--bg-mute);border-radius:10px;padding:12px 16px;margin:20px 0}')
    t = rep(t, '.tile{background:var(--bg-soft);border-radius:10px;padding:14px 16px}',
            '.tile{background:var(--bg-elv);border:1px solid var(--divider);border-radius:12px;padding:14px 16px}')

    # 18) 移动端标题字号与 index.html 对齐
    t = rep(t, '  h1{font-size:24px}', '  h1{font-size:27px;line-height:1.35}')

    with open(sp, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print('restyled selfcheck.html')

print('ALL OK')
