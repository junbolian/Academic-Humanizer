#!/usr/bin/env python3
"""
check_revision.py (academic-humanizer v1.0)

Deterministic checks behind the skill's promises, so that "no number, citation or
equation was changed" is verified rather than self-reported.

  python3 check_revision.py audit FILE
  python3 check_revision.py compare ORIGINAL REVISED [--changes]

audit    Candidate AI-tell phrases (from ../references/lexicon.txt), [[EVIDENCE: ...]]
         placeholders, sentence patterns (adjacent sentences with one skeleton, dense
         inline lists, list lead-in lines, ordinal headings, paragraph openings without
         a referent, signpost connectives opening consecutive paragraphs, paragraphs
         crowded with semicolons or parenthetical asides), dashes used as punctuation, sentences over the length limit, runs of very short sentences,
         stacked additive connectives, and the section/result structure of LaTeX or
         Markdown input.
compare  Checks that numbers, citation keys, \\ref/\\label keys, math, the text of formal
         environments (definition, assumption, theorem, proposition, lemma, corollary,
         ...) and the LaTeX preamble are unchanged. Then reports conservation warnings
         (qualifiers that disappeared, capitalized terms and quoted strings that are new)
         and how many sentences changed; --changes prints every changed sentence so that
         each can be matched to a rule. Finally audits REVISED with counts relative to
         ORIGINAL. Exit status 1 if any invariant changed; warnings do not change the
         exit status. The contents of [[EVIDENCE: ...]] placeholders are excluded from
         these checks and listed.

Every audit hit is a candidate for review, not a verdict. Standard library only.
"""
import argparse
import collections
import difflib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LEXICON = os.path.normpath(os.path.join(HERE, '..', 'references', 'lexicon.txt'))

MATH_ENVS = ['equation', 'align', 'alignat', 'gather', 'multline', 'flalign',
             'eqnarray', 'displaymath', 'math', 'dmath', 'dgroup']
FORMAL_ENVS = {'definition', 'defn', 'dfn', 'assumption', 'assumptions', 'assump', 'asm',
               'theorem', 'thm', 'proposition', 'prop', 'lemma', 'lem', 'corollary',
               'cor', 'coro', 'conjecture', 'conj', 'claim', 'hypothesis', 'axiom',
               'condition'}
RESULT_ENVS = {'theorem', 'thm', 'proposition', 'prop', 'lemma', 'lem', 'corollary',
               'cor', 'coro'}
NONPROSE_ENVS = ['tabular', 'tabularx', 'tabulary', 'longtable', 'supertabular',
                 'algorithm', 'algorithmic', 'algorithm2e', 'lstlisting', 'verbatim',
                 'Verbatim', 'minted', 'tikzpicture', 'thebibliography', 'filecontents',
                 'comment']
MPH = '\u27e8M\u27e9'        # placeholder for one math segment in prose
PARA = ' \u00b6 '            # sentence boundary marker
TITLE = '\u00a7'             # marks a heading or caption fragment

CITE_RE = re.compile(r'\\(?:[A-Za-z]*cite[A-Za-z]*)\*?\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}')
REF_RE = re.compile(r'\\(ref|eqref|cref|Cref|crefrange|Crefrange|autoref|Autoref|pageref|'
                    r'nameref|vref|Vref|labelcref|label)\*?\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}')
NUM_RE = re.compile(r'(?:(?<=[\s(\[{~])[-\u2212]|(?<![A-Za-z0-9_.\\]))\d+(?:[.,]\d+)*(?:\\?%)?')
NAME = r"[A-Z][A-Za-z'\u00C0-\u017F\-]+"
AY_NARR = re.compile('(' + NAME + r')(?:\s+(?:and|&)\s+' + NAME + r')?(?:\s+et\s+al\.)?\s*\((\d{4}[a-z]?)\)')
AY_PAREN = re.compile(r'\(([^()]*\d{4}[a-z]?[^()]*)\)')
AY_ITEM = re.compile('(' + NAME + r')(?:\s+(?:and|&)\s+' + NAME + r')?(?:\s+et\s+al\.)?,?\s+(\d{4}[a-z]?)')
NUMCITE = re.compile(r'\[(\d+(?:\s*[-\u2013,]\s*\d+)*)\]')
PANDOC_CITE = re.compile(r'\[(?:[^\[\]]*?[\s;-])?@[A-Za-z0-9_][^\[\]]*\]')
PANDOC_KEY = re.compile(r'(?<![A-Za-z0-9_.])@([A-Za-z0-9_][A-Za-z0-9_:.#$%&+?<>~/-]*)')
BEGIN_ANY = re.compile(r'\\begin\{([A-Za-z]+)(\*?)\}')
SECT_RE = re.compile(r'\\(part|chapter|section|subsection|subsubsection|paragraph|caption)(\*?)\s*(?:\[[^\]]*\])?\s*(?=\{)')
ADDITIVE = re.compile(r'^(moreover|furthermore|additionally|in addition|also|besides)\b', re.I)
CJK = re.compile(r'[\u4e00-\u9fff]')
PLACEHOLDER_RE = re.compile(r'\[\[EVIDENCE:.*?\]\]', re.S)

# sentence-pattern checks (SKILL.md Rule 4; references/chinese.md Rule 11)
ZH_COMMENT_OPEN = re.compile(r'^(?:听起来|看起来|看上去|听上去|说白了|说到底|换句话说|意味着|值得注意|'
                             r'不难看出|问题在于|原因在于|结果是|有意思的是|更重要的是|关键在于|真正的)')
ZH_ANAPHOR = re.compile(r'[这那其此]|上述|上面|前面|以上|该')
EN_COMMENT_OPEN = re.compile(r'^(?:more importantly|most importantly|the catch is|the problem is|'
                             r'the key is|what is more|even more)\b', re.I)
SIGNPOST_ZH = re.compile(r'^(?:然而|因此|此外|与此同时|换言之|总而言之|综上所述)[，、,]')
SIGNPOST_EN = re.compile(r'^(?:moreover|furthermore|additionally|in addition|however|therefore|'
                         r'thus|hence|consequently|meanwhile|in summary|overall)\b', re.I)
ORDINAL_HEAD = re.compile(r'^\s*(?:第?[一二三四五六七八九十]+[、.．:：]|第[一二三四五六七八九十]+(?=\S)|'
                          r'(?:first|second|third|fourth|fifth|sixth)\b[,:.]?)', re.I)
LIST_ITEM = re.compile(r'^\s*(?:[-*+\u2022]\s+|\d+[.)\u3001]\s*|[一二三四五六七八九十]+\u3001|'
                       r'\\begin\{(?:itemize|enumerate|description)\}|\\item\b)')
# qualifiers and concessions whose loss strengthens a claim (edit discipline, item 4)
QUAL_EN = re.compile(r"\b(?:may|might|could|likely|unlikely|possibly|potentially|perhaps|probably|"
                     r"suggests?|suggested|suggesting|appears? to|appeared to|seems? to|seemed to|"
                     r"tends? to|tended to|typically|usually|often|generally|in general|in some cases|"
                     r"in most cases|approximately|roughly|we conjecture|conjecture[sd]?|is consistent with|"
                     r"are consistent with|under (?:these|this|the stated|mild) (?:conditions?|assumptions?))\b", re.I)
QUAL_ZH = re.compile(r'可能|或许|也许|大概|大致|通常|一般而言|一般来说|往往|多数情况下|在某些情况下|'
                     r'在一定条件下|在一定程度上|据说|似乎|倾向于|提示(?!词)|与[^，。]{1,12}一致|约(?=\s*\d)|左右')
CAP_TOKEN = re.compile(r"\b[A-Z][A-Za-z0-9&'\-]*[A-Za-z0-9]\b")
WORD_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9&'\-]*")
QUOTE_RES = [re.compile(r'\u201c([^\u201d\n]{1,120})\u201d'), re.compile(r'\u300c([^\u300d\n]{1,120})\u300d'),
             re.compile(r'\u300e([^\u300f\n]{1,120})\u300f'), re.compile(r"``([^'\n]{1,120})''"),
             re.compile(r'(?<![A-Za-z0-9])"([^"\n]{1,120})"')]

ABBREV = ['e.g.', 'i.e.', 'et al.', 'etc.', 'vs.', 'cf.', 'Fig.', 'Figs.', 'Eq.', 'Eqs.',
          'Sec.', 'Secs.', 'Tab.', 'Ref.', 'Refs.', 'Prop.', 'Props.', 'Thm.', 'Def.',
          'Cor.', 'Lem.', 'Assump.', 'App.', 'Ch.', 'resp.', 'approx.', 'No.', 'Nos.',
          'pp.', 'p.', 'Dr.', 'Prof.', 'Mr.', 'Ms.', 'St.', 'U.S.', 'U.K.', 'Inc.',
          'Ltd.', 'Co.', 'Jr.', 'Sr.', 'Vol.', 'vol.', 'ed.', 'eds.', 'Corp.']
ABBREV_RE = re.compile(r'(?<![A-Za-z])(' + '|'.join(re.escape(a) for a in ABBREV) + ')')
SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9\u27e8(\[\u201c"\\])')


# ---------------------------------------------------------------- helpers

def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read().replace('\r\n', '\n').replace('\r', '\n')


def newlines(s):
    return '\n' * s.count('\n')


def sub_keep(pattern, repl, text, flags=0):
    """re.sub that keeps the newline count of every replaced span (stable line numbers)."""
    rx = pattern if hasattr(pattern, 'sub') else re.compile(pattern, flags)

    def f(m):
        r = repl(m) if callable(repl) else repl
        return r + newlines(m.group(0))
    return rx.sub(f, text)


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def clip(s, n=110):
    s = ' '.join(s.split())
    return s if len(s) <= n else s[:n - 3] + '...'


def window(line, start, end, width=45):
    """Text around line[start:end], with the match marked by >>...<<."""
    a, b = max(0, start - width), min(len(line), end + width)
    pre = ('...' if a > 0 else '') + line[a:start]
    post = line[end:b] + ('...' if b < len(line) else '')
    return ' '.join((pre + '>>' + line[start:end] + '<<' + post).split())


def strip_comments(text):
    out = []
    for line in text.split('\n'):
        i, n, cut = 0, len(line), len(line)
        while i < n:
            c = line[i]
            if c == '\\':
                i += 2
                continue
            if c == '%':
                cut = i
                break
            i += 1
        out.append(line[:cut])
    return '\n'.join(out)


def body_only(text):
    """Blank the preamble and anything after \\end{document}; keep line numbers."""
    b = text.find('\\begin{document}')
    if b == -1:
        return text, None
    e = text.find('\\end{document}', b)
    if e == -1:
        e = len(text)
    return newlines(text[:b]) + text[b:e] + newlines(text[e:]), text[:b]


def read_braced(text, i):
    """text[i] == '{'. Return index just past the matching '}'."""
    depth, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '\\':
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def split_math(text, latex):
    """Return (prose, segments). Each math segment is replaced by MPH plus its newlines."""
    env_begin = re.compile(r'\\begin\{(' + '|'.join(MATH_ENVS) + r')(\*?)\}')
    segs, out = [], []
    i, n = 0, len(text)

    def emit(k):
        seg = text[i:k]
        segs.append(seg)
        out.append(MPH + newlines(seg))
        return k

    while i < n:
        c = text[i]
        if c == '\\':
            m = env_begin.match(text, i)
            if m:
                end_tok = '\\end{%s%s}' % (m.group(1), m.group(2))
                j = text.find(end_tok, m.end())
                i = emit(n if j == -1 else j + len(end_tok))
                continue
            nxt = text[i + 1:i + 2]
            if nxt in ('[', '('):
                end_tok = '\\]' if nxt == '[' else '\\)'
                j = text.find(end_tok, i + 2)
                i = emit(n if j == -1 else j + 2)
                continue
            out.append(text[i:i + 2])
            i += 2
            continue
        if c == '$':
            if text[i + 1:i + 2] == '$':
                j = text.find('$$', i + 2)
                i = emit(n if j == -1 else j + 2)
                continue
            limit = text.find('\n\n', i)
            limit = n if limit == -1 else limit
            j = i + 1
            while j < limit and text[j] != '$':
                j += 2 if text[j] == '\\' else 1
            inner = text[i + 1:j]
            closed = j < limit and text[j:j + 1] == '$'
            looks_math = closed and inner and (latex or (not inner[0].isspace() and not inner[-1].isspace()))
            if looks_math:
                i = emit(j + 1)
                continue
        out.append(c)
        i += 1
    return ''.join(out), segs


def mask_envs(text, names):
    pat = re.compile(r'\\begin\{(' + '|'.join(map(re.escape, names)) + r')(\*?)\}')
    out, i = [], 0
    while True:
        m = pat.search(text, i)
        if not m:
            out.append(text[i:])
            return ''.join(out)
        end_tok = '\\end{%s%s}' % (m.group(1), m.group(2))
        j = text.find(end_tok, m.end())
        k = len(text) if j == -1 else j + len(end_tok)
        out.append(text[i:m.start()])
        out.append(newlines(text[m.start():k]))
        i = k


def headings_to_markers(text):
    """Turn \\section{...}, \\caption{...} etc. into standalone fragments."""
    out, i = [], 0
    for m in SECT_RE.finditer(text):
        if m.start() < i:
            continue
        k = read_braced(text, m.end())
        title = text[m.end() + 1:k - 1]
        out.append(text[i:m.start()])
        out.append(PARA + TITLE + ' ' + title.replace('\n', ' ') + PARA + newlines(title))
        i = k
    out.append(text[i:])
    return ''.join(out)


def latex_scan_text(masked):
    t = sub_keep(CITE_RE, ' [cite] ', masked)
    t = sub_keep(REF_RE, lambda m: '' if m.group(1) == 'label' else '[ref]', t)
    t = sub_keep(r'\\(?:url|href|includegraphics|input|include|bibliography|bibliographystyle|'
                 r'vspace|hspace|setlength|addtolength|newcommand|renewcommand|usepackage|'
                 r'documentclass)\*?\s*(?:\[[^\]]*\])?\s*\{[^}]*\}', '', t)
    t = headings_to_markers(t)
    t = sub_keep(r'\\begin\{[^}]*\}(?:\[[^\]]*\])?|\\end\{[^}]*\}|\\item\b(?:\[[^\]]*\])?|'
                 r'\\par\b|\\\\(?:\[[^\]]*\])?|\\maketitle\b|\\appendix\b', PARA, t)
    t = t.replace('~', ' ').replace('\\%', '%').replace('\\&', '&').replace('\\$', '$')
    t = re.sub(r'\\[A-Za-z@]+\*?', '', t)
    t = t.replace('{', '').replace('}', '')
    return t


def markdown_scan_text(masked):
    t = sub_keep(r'```.*?```', '', masked, re.S)
    t = re.sub(r'(?m)^(#{1,6})\s+(.*)$', lambda m: PARA + TITLE + ' ' + m.group(2) + PARA, t)
    t = re.sub(r'(?m)^\s*(?:[-*+]|\d+\.)\s+', PARA, t)
    return t


# ---------------------------------------------------------------- analysis

class Doc:
    def __init__(self, path):
        self.path = path
        raw = read(path)
        low = path.lower()
        self.markdown = low.endswith(('.md', '.markdown', '.qmd', '.rmd'))
        self.latex = (not self.markdown) and (low.endswith(('.tex', '.ltx')) or bool(re.search(
            r'\\(documentclass|begin\{document\}|section\*?\{|cite[pt]?\{|begin\{(equation|align|proposition|theorem))', raw)))
        text = strip_comments(raw) if self.latex else raw
        if self.markdown and text.startswith('---\n'):
            end = text.find('\n---\n', 4)
            if end != -1:                           # YAML front matter is metadata, not prose
                text = newlines(text[:end + 5]) + text[end + 5:]
        self.preamble = None
        if self.latex:
            text, self.preamble = body_only(text)
        self.body = text
        cjk = len(CJK.findall(text))
        latin = len(re.findall(r'[A-Za-z]', text))
        self.chinese = cjk > 0.3 * (cjk + latin) if (cjk + latin) else False
        # [[EVIDENCE: ...]] placeholders are listed separately; their contents are not
        # counted as numbers, citations or math, so inserting one is not a false difference.
        self.placeholders = [(' '.join(m.group(0).split()), line_of(text, m.start()))
                             for m in PLACEHOLDER_RE.finditer(text)]
        text = sub_keep(PLACEHOLDER_RE, ' ', text)
        self.prose, self.math = split_math(text, self.latex)
        scan = mask_envs(self.prose, NONPROSE_ENVS) if self.latex else self.prose
        if self.latex:
            self.scan = latex_scan_text(scan)
        elif self.markdown:
            self.scan = markdown_scan_text(scan)
        else:
            self.scan = scan
        self._extract()

    # invariants -------------------------------------------------
    def _extract(self):
        p = self.prose
        self.cites, self.refs, self.numbers = [], [], []
        if self.latex:
            for m in CITE_RE.finditer(p):
                for key in m.group(1).split(','):
                    if key.strip():
                        self.cites.append((key.strip(), line_of(p, m.start())))
            for m in REF_RE.finditer(p):
                kind = 'label' if m.group(1) == 'label' else 'ref'
                for key in m.group(2).split(','):
                    if key.strip():
                        self.refs.append((kind + ':' + key.strip(), line_of(p, m.start())))
            numtext = sub_keep(CITE_RE, ' ', p)
            numtext = sub_keep(REF_RE, ' ', numtext)
        else:
            for m in CITE_RE.finditer(p):           # LaTeX citation commands inside Markdown or plain text
                for key in m.group(1).split(','):
                    if key.strip():
                        self.cites.append((key.strip(), line_of(p, m.start())))
            for m in REF_RE.finditer(p):
                kind = 'label' if m.group(1) == 'label' else 'ref'
                for key in m.group(2).split(','):
                    if key.strip():
                        self.refs.append((kind + ':' + key.strip(), line_of(p, m.start())))
            for m in PANDOC_CITE.finditer(p):       # Pandoc/Quarto citations: [@key; @key2, p. 4]
                for key in PANDOC_KEY.findall(m.group(0)):
                    self.cites.append(('@' + key.rstrip('.:'), line_of(p, m.start())))
            for m in AY_NARR.finditer(p):
                self.cites.append((m.group(1) + ' ' + m.group(2), line_of(p, m.start())))
            for m in AY_PAREN.finditer(p):
                for part in m.group(1).split(';'):
                    a = AY_ITEM.search(part)
                    if a:
                        self.cites.append((a.group(1) + ' ' + a.group(2), line_of(p, m.start())))
            for m in NUMCITE.finditer(p):
                for item in m.group(1).split(','):
                    self.cites.append(('[' + re.sub(r'\s', '', item) + ']', line_of(p, m.start())))
            numtext = sub_keep(CITE_RE, ' ', p)
            numtext = sub_keep(REF_RE, ' ', numtext)
            numtext = sub_keep(PANDOC_CITE, ' ', numtext)
        for m in NUM_RE.finditer(numtext):
            tok = m.group(0).replace('\u2212', '-').replace('\\%', '%')
            ln = line_of(numtext, m.start())
            ls = numtext.rfind('\n', 0, m.start()) + 1
            le = numtext.find('\n', m.end())
            line = numtext[ls:(len(numtext) if le == -1 else le)]
            self.numbers.append((tok, ln, window(line, m.start() - ls, m.end() - ls, 40)))
        self.formal = []
        if self.latex:
            b = self.body
            for m in BEGIN_ANY.finditer(b):
                name = m.group(1)
                if name.lower() not in FORMAL_ENVS:
                    continue
                end_tok = '\\end{%s%s}' % (name, m.group(2))
                j = b.find(end_tok, m.end())
                if j != -1:
                    self.formal.append((name.lower(), ' '.join(b[m.end():j].split()),
                                        line_of(b, m.start())))

    # audit pieces -----------------------------------------------
    def lexicon_hits(self, lex):
        hits = []
        lines = self.scan.split('\n')
        for ln, line in enumerate(lines, 1):
            clean = line.replace(PARA.strip(), ' ').replace(TITLE, ' ')
            for cat, rx in lex.patterns:
                for m in rx.finditer(clean):
                    hits.append((cat, m.group(0).lower(), ln, window(clean, m.start(), m.end())))
        return hits

    def dash_hits(self):
        def em(m):
            s, line = m.group(0), m.string
            if len(s) >= 2:
                return 'Chinese 破折号 or doubled em dash'
            before, after = line[m.start() - 1:m.start()], line[m.end():m.end() + 1]
            if before.isdigit() and after.isdigit():
                return None                      # range such as 2011\u20142015
            if self.chinese:
                return 'single U+2014 (keep only as a 连接号 for a span such as 北京\u2014上海)'
            return 'em dash (U+2014)'
        pats = [(em, re.compile('\u2014+')),
                ('spaced en dash used as a dash', re.compile(r'(?<=\S) (?:--|\u2013) (?=\S)')),
                ('spaced hyphen used as a dash', re.compile(r'(?<=[A-Za-z,)]) - (?=[A-Za-z(])'))]
        if self.latex:
            pats.insert(1, ('LaTeX em dash ---', re.compile(r'(?<!-)---(?!-)')))
        hits = []
        for ln, line in enumerate(self.scan.split('\n'), 1):
            clean = line.replace(PARA.strip(), ' ').replace(TITLE, ' ')
            for name, rx in pats:
                for m in rx.finditer(clean):
                    label = name(m) if callable(name) else name
                    if label:
                        hits.append((label, ln, window(clean, m.start(), m.end())))
        return hits

    def sentences(self):
        """Return (paragraph_index, line, sentence) for each prose sentence."""
        out, para_idx = [], 0
        mark = PARA.strip()

        def flush(chunk):
            nonlocal para_idx
            if not chunk:
                return
            text, offsets, pos = '', [], 0
            for ln, line in chunk:
                offsets.append((len(text), ln))
                text += line.strip() + ' '
            def line_at(k):
                cur = offsets[0][1]
                for off, ln in offsets:
                    if off <= k:
                        cur = ln
                    else:
                        break
                return cur
            blocks, start = [], 0
            for m in re.finditer(re.escape(mark), text):
                blocks.append((start, text[start:m.start()]))
                start = m.end()
            blocks.append((start, text[start:]))
            for b0, block in blocks:
                if not block.strip():
                    continue
                if self.chinese:
                    spans, prev = [], 0
                    for m in re.finditer(r'(?<=[。！？])', block):
                        spans.append((prev, m.start()))
                        prev = m.start()
                    spans.append((prev, len(block)))
                else:
                    prot = ABBREV_RE.sub(lambda m: m.group(1).replace('.', '\u2024'), block)
                    spans, prev = [], 0
                    for m in SENT_SPLIT.finditer(prot):
                        spans.append((prev, m.start()))
                        prev = m.end()
                    spans.append((prev, len(block)))
                for a, b in spans:
                    sent = block[a:b].strip()
                    if sent:
                        lead = len(block[a:b]) - len(block[a:b].lstrip())
                        out.append((para_idx, line_at(b0 + a + lead), sent))
                para_idx += 1

        chunk = []
        for ln, line in enumerate(self.scan.split('\n'), 1):
            if line.strip() == '':
                flush(chunk)
                chunk = []
            else:
                chunk.append((ln, line))
        flush(chunk)
        return out

    def paragraphs(self):
        """Prose paragraphs as lists of (line, sentence); headings are excluded and mark breaks."""
        paras, cur, cur_idx = [], [], None
        for p, ln, s in self.sentences():
            if s.startswith(TITLE):
                if cur:
                    paras.append(cur)
                cur, cur_idx = [], None
                paras.append(None)                  # heading marker
                continue
            if cur_idx is not None and p != cur_idx and cur:
                paras.append(cur)
                cur = []
            cur_idx = p
            cur.append((ln, s))
        if cur:
            paras.append(cur)
        return paras

    def _signature(self, s):
        s2 = s.replace(MPH, 'x')
        if self.chinese:
            if len(s2) <= 10 or s2.count('\uff0c') < 1:
                return None
            return (s2.count('\uff0c'), '\uff1a' in s2, '\uff08' in s2 or '(' in s2, len(s2) // 15)
        words = s2.split()
        if len(words) < 8 or s2.count(',') < 1:
            return None
        return (s2.count(','), (':' in s2) or (';' in s2), '(' in s2, len(words) // 6)

    def pattern_checks(self):
        out = collections.OrderedDict()
        paras = self.paragraphs()
        prose = [pp for pp in paras if pp]
        # adjacent sentences with one skeleton (Rule 4.3)
        pairs, runs = 0, []
        for pp in prose:
            sigs = [self._signature(s) for _, s in pp]
            i = 0
            while i < len(sigs) - 1:
                j = i
                while j + 1 < len(sigs) and sigs[i] is not None and sigs[j + 1] == sigs[i]:
                    j += 1
                if j > i:
                    pairs += j - i
                    if j - i + 1 >= 3:
                        runs.append((pp[i][0], ' | '.join(clip(s, 45) for _, s in pp[i:j + 1])))
                    i = j
                i += 1
        out['adjacent sentences with one skeleton (4.3)'] = (
            '%d adjacent pairs; runs of 3+ listed' % pairs, runs)
        # dense inline lists, Chinese (4.5)
        if self.chinese:
            dense = []
            for pp in prose:
                for ln, s in pp:
                    for clause in re.split(r'[\uff0c\uff1b\uff1a\u3002\uff01\uff1f,;:]', s):
                        if clause.count('\u3001') >= 2:
                            dense.append((ln, clip(clause, 70)))
            out['clauses with 2+ 顿号 (4.5, keep content lists)'] = ('%d' % len(dense), dense)
        # paragraph openings without a referent (4.7), skipping the first paragraph
        noref = []
        for k, pp in enumerate(prose):
            if k == 0:
                continue
            ln, first = pp[0]
            if self.chinese:
                if ZH_COMMENT_OPEN.match(first) and not ZH_ANAPHOR.search(first[:12]):
                    noref.append((ln, clip(first, 70)))
            elif EN_COMMENT_OPEN.match(first):
                noref.append((ln, clip(first, 70)))
        out['paragraph opens with a comment, no referent (4.7)'] = ('%d' % len(noref), noref)
        # signpost connectives opening consecutive paragraphs (4.8)
        sp, prev = [], None
        for pp in paras:
            if not pp:
                prev = None
                continue
            ln, first = pp[0]
            hit = (SIGNPOST_ZH if self.chinese else SIGNPOST_EN).match(first)
            if hit and prev is not None:
                sp.append((ln, '%s | %s' % (clip(prev, 40), clip(first, 40))))
            prev = first if hit else None
        out['consecutive paragraphs opening with a signpost (4.8)'] = ('%d' % len(sp), sp)
        # semicolons and parenthetical asides per paragraph (Rule 3)
        crowded = []
        aside_rx = re.compile(r'[(（]([^()（）]{1,200})[)）]')
        for pp in prose:
            text = ' '.join(s for _, s in pp)
            semis = text.count(';') + text.count('；')
            asides = 0
            for m in aside_rx.finditer(text):
                inner = m.group(1).strip()
                if re.fullmatch(r'(\[cite\]|\[ref\]|' + re.escape(MPH) + r'|[\d.,%\s\-–]+|[A-Za-z]?\d+[a-z]?|'
                                r'(?:see |cf\. )?(?:Table|Figure|Fig\.|Section|Sec\.|Eq\.|Appendix|Theorem|'
                                r'Proposition|Lemma|Corollary|Assumption|Definition|Example|表|图|定理|命题|引理|假设|附录|第)'
                                r'[^)）]{0,40}|.*\[cite\].*|.*\[ref\].*)', inner):
                    continue
                asides += 1
            if semis >= 2 or (asides >= 3 and asides * 2 >= len(pp)):
                crowded.append((pp[0][0], '%d semicolon(s), %d aside(s): %s' % (semis, asides, clip(text, 60))))
        out['paragraphs crowded with semicolons or asides (Rule 3)'] = ('%d' % len(crowded), crowded)
        # list lead-in lines and ordinal headings work on raw lines (4.2, 4.6)
        lines = self.body.split('\n')
        leads = []
        for i, line in enumerate(lines):
            st = line.strip()
            if not st or st.startswith(('#', '|', '>', '%')) or LIST_ITEM.match(st):
                continue
            if st.endswith(('\uff1a', ':')) and not st.endswith('::'):
                nxt = next((l for l in lines[i + 1:] if l.strip()), '')
                if LIST_ITEM.match(nxt):
                    leads.append((i + 1, clip(st, 70)))
        out['line ending in a colon before a list (4.2; verify)'] = ('%d' % len(leads), leads)
        heads = []
        for i, line in enumerate(lines):
            st = line.strip()
            m = re.match(r'^(#{1,6})\s+(.*)$', st)
            if m:
                heads.append((i + 1, 'h%d' % len(m.group(1)), m.group(2)))
                continue
            m = re.match(r'^\*\*([^*]{1,60})\*\*$', st)
            if m:
                heads.append((i + 1, 'bold', m.group(1)))
                continue
            m = re.match(r'^\\(section|subsection|subsubsection)\*?\s*\{(.*)\}', st)
            if m:
                heads.append((i + 1, m.group(1), m.group(2)))
        ords, run = [], []
        for h in heads + [(None, None, '')]:
            if h[0] is not None and ORDINAL_HEAD.match(h[2]) and (not run or run[-1][1] == h[1]):
                run.append(h)
                continue
            if len(run) >= 3:
                ords.append((run[0][0], ' | '.join(clip(x[2], 30) for x in run)))
            run = [h] if (h[0] is not None and ORDINAL_HEAD.match(h[2])) else []
        out['ordinal headings, 3+ in a row (4.6; not manuscript numbering)'] = ('%d' % len(ords), ords)
        return out

    def structure(self):
        rows = []
        if self.latex:
            b = self.body
            app = len(b)
            for tok in ('\\appendix', '\\begin{appendices}'):
                k = b.find(tok)
                if k != -1:
                    app = min(app, k)
            levels = {'part': 0, 'chapter': 1, 'section': 2, 'subsection': 3,
                      'subsubsection': 4, 'paragraph': 5}
            for m in SECT_RE.finditer(b):
                if m.group(1) == 'caption':
                    continue
                k = read_braced(b, m.end())
                rows.append((levels[m.group(1)], ' '.join(b[m.end() + 1:k - 1].split()),
                             line_of(b, m.start()), m.start() >= app))
            results = collections.Counter()
            for name, _, ln in self.formal:
                pos_app = self._line_in_appendix(ln, app)
                results[('appendix' if pos_app else 'main', name)] += 1
            return rows, results, app < len(b)
        if self.markdown:
            for ln, line in enumerate(self.body.split('\n'), 1):
                m = re.match(r'^(#{1,6})\s+(.*)$', line)
                if m:
                    rows.append((len(m.group(1)), m.group(2).strip(), ln, False))
        return rows, collections.Counter(), False

    def _line_in_appendix(self, ln, app_pos):
        return ln >= line_of(self.body, app_pos) if app_pos < len(self.body) else False


class Lexicon:
    def __init__(self, path):
        self.patterns, self.kind, self.desc = [], {}, {}
        with open(path, encoding='utf-8') as f:
            for raw in f:
                line = raw.rstrip('\r\n')
                if not line.strip() or line.lstrip().startswith('#'):
                    continue
                if line.startswith('@'):
                    parts = line[1:].split(None, 2)
                    self.kind[parts[0]] = parts[1] if len(parts) > 1 else 'remove'
                    self.desc[parts[0]] = parts[2] if len(parts) > 2 else ''
                    continue
                parts = line.split(None, 1)
                if len(parts) < 2:
                    continue
                self.patterns.append((parts[0], re.compile(parts[1], re.I)))


# ---------------------------------------------------------------- reporting

def print_counter_diff(label, a_items, b_items, show_ctx=True):
    ca = collections.Counter(t for t, *_ in a_items)
    cb = collections.Counter(t for t, *_ in b_items)
    if ca == cb:
        print('  %-34s unchanged (%d)' % (label, sum(ca.values())))
        return True
    removed, added = ca - cb, cb - ca
    print('  %-34s CHANGED (%d -> %d)' % (label, sum(ca.values()), sum(cb.values())))
    for title, diff, items in (('removed or changed', removed, a_items), ('added', added, b_items)):
        if not diff:
            continue
        print('    %s:' % title)
        for tok, cnt in sorted(diff.items(), key=lambda x: str(x[0]))[:30]:
            locs = [it for it in items if it[0] == tok][:2]
            where = '; '.join('line %d%s' % (it[1], (': ' + it[2]) if show_ctx and len(it) > 2 else '')
                              for it in locs)
            print('      %s  x%d  [%s]' % (clip(tok, 60), cnt, where))
        if len(diff) > 30:
            print('      ... %d more' % (len(diff) - 30))
    return False


def compare_math(A, B):
    na = collections.Counter(' '.join(s.split()) for s in A.math)
    nb = collections.Counter(' '.join(s.split()) for s in B.math)
    if na == nb:
        print('  %-34s unchanged (%d segments)' % ('math', sum(na.values())))
        return True
    print('  %-34s CHANGED (%d -> %d segments)' % ('math', sum(na.values()), sum(nb.values())))
    for title, diff in (('removed or changed', na - nb), ('added', nb - na)):
        if diff:
            print('    %s:' % title)
            for seg, cnt in list(diff.items())[:20]:
                print('      x%d  %s' % (cnt, clip(seg, 120)))
    return False


def compare_formal(A, B):
    fa = [(n, t) for n, t, _ in A.formal]
    fb = [(n, t) for n, t, _ in B.formal]
    if fa == fb:
        print('  %-34s unchanged (%d)' % ('formal statements', len(fa)))
        return True
    print('  %-34s CHANGED' % 'formal statements')
    if [n for n, _ in fa] != [n for n, _ in fb]:
        print('    environment sequence differs: %s -> %s' % (
            dict(collections.Counter(n for n, _ in fa)), dict(collections.Counter(n for n, _ in fb))))
    for (na_, ta), (nb_, tb), (_, _, ln) in zip(fa, fb, B.formal):
        if na_ == nb_ and ta != tb:
            wa, wb = ta.split(), tb.split()
            sm = difflib.SequenceMatcher(a=wa, b=wb)
            edits = ['-[%s] +[%s]' % (clip(' '.join(wa[i1:i2]), 60), clip(' '.join(wb[j1:j2]), 60))
                     for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
            print('    %s at revised line %d: %s' % (nb_, ln, '; '.join(edits[:4])))
    return False


def quoted(D):
    out = []
    for rx in QUOTE_RES:
        for m in rx.finditer(D.scan):
            out.append((' '.join(m.group(1).split()), line_of(D.scan, m.start())))
    return out


def _units(s):
    return list(s) if CJK.search(s) else re.findall(r"\w+|[^\w\s]", s.lower())


def _sim(a, b):
    return difflib.SequenceMatcher(a=_units(a), b=_units(b), autojunk=False).ratio()


def _align_block(A_, B_):
    """Minimum-cost alignment of two short sentence lists with match, delete, insert, merge (2 to 1)
    and split (1 to 2) steps; returns the steps in order."""
    D = 0.35
    n, m = len(A_), len(B_)
    INF = float('inf')
    cost = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    cost[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            c = cost[i][j]
            if c == INF:
                continue
            steps = []
            if i < n:
                steps.append((i + 1, j, D, 'removed'))
            if j < m:
                steps.append((i, j + 1, D, 'added'))
            if i < n and j < m:
                steps.append((i + 1, j + 1, 1 - _sim(A_[i][1], B_[j][1]), 'changed'))
            if i + 1 < n and j < m:
                steps.append((i + 2, j + 1, 1.2 - _sim(A_[i][1] + ' ' + A_[i + 1][1], B_[j][1]), 'merged'))
            if i < n and j + 1 < m:
                steps.append((i + 1, j + 2, 1.2 - _sim(A_[i][1], B_[j][1] + ' ' + B_[j + 1][1]), 'split'))
            for i2, j2, w, kind in steps:
                if c + w < cost[i2][j2]:
                    cost[i2][j2] = c + w
                    back[i2][j2] = (i, j, kind)
    out, i, j = [], n, m
    while (i, j) != (0, 0):
        pi, pj, kind = back[i][j]
        out.append((kind, A_[pi:i], B_[pj:j]))
        i, j = pi, pj
    return out[::-1]


def sentence_changes(sa, sb):
    """Align sentences; return [(kind, [(line, old)...], [(line, new)...])] for every non-identical unit.
    kind is changed (one to one), merged (two to one), split (one to two), added, or removed."""
    out = []
    sm = difflib.SequenceMatcher(a=[s for _, s in sa], b=[s for _, s in sb], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        if (i2 - i1) * (j2 - j1) > 40000:            # very large block: report it whole
            out.append(('changed', sa[i1:i2], sb[j1:j2]))
            continue
        out.extend(_align_block(sa[i1:i2], sb[j1:j2]))
    return out


def conservation(A, B, show_changes):
    """Warnings for the edit discipline: lost qualifiers, new names, new quotations, changed sentences."""
    print('\n== Conservation warnings (do not affect the exit status) ==')
    warn = 0
    qa, qb = [], []
    for D, acc in ((A, qa), (B, qb)):
        rx = QUAL_ZH if D.chinese else QUAL_EN
        for m in rx.finditer(D.scan):
            ln = line_of(D.scan, m.start())
            ls = D.scan.rfind('\n', 0, m.start()) + 1
            le = D.scan.find('\n', m.end())
            line = D.scan[ls:(len(D.scan) if le == -1 else le)].replace(PARA.strip(), ' ')
            acc.append((m.group(0).lower(), ln, window(line, m.start() - ls, m.end() - ls, 40)))
    ca = collections.Counter(q for q, *_ in qa)
    cb = collections.Counter(q for q, *_ in qb)
    lost = ca - cb
    print('  qualifiers and concessions: %d -> %d' % (sum(ca.values()), sum(cb.values())))
    if lost:
        warn += 1
        print('    LOST (each one strengthens a claim unless it was intended):')
        for q, n in sorted(lost.items()):
            for _, ln, ctx in [x for x in qa if x[0] == q][:2]:
                print('      %s x%d  original line %d: %s' % (q, n, ln, ctx))
    a_words = set(WORD_TOKEN.findall(A.scan))
    a_lower = {w.lower() for w in a_words}
    new_caps = collections.OrderedDict()
    for m in CAP_TOKEN.finditer(B.scan):
        tok = m.group(0)
        if tok not in a_words and tok.lower() not in a_lower and tok not in new_caps:
            new_caps[tok] = line_of(B.scan, m.start())
    print('  capitalized terms not in the original: %d' % len(new_caps))
    if new_caps:
        warn += 1
        print('      ' + ', '.join('%s (line %d)' % kv for kv in list(new_caps.items())[:40]))
    aq = {q for q, _ in quoted(A)}
    nq = [(q, ln) for q, ln in quoted(B) if q not in aq]
    print('  quoted strings not in the original: %d' % len(nq))
    if nq:
        warn += 1
        for q, ln in nq[:20]:
            print('      line %d: "%s"' % (ln, clip(q, 80)))
    sa = [(ln, ' '.join(s.split())) for _, ln, s in A.sentences()]
    sb = [(ln, ' '.join(s.split())) for _, ln, s in B.sentences()]
    changes = sentence_changes(sa, sb)
    same = len(sa) - sum(len(c[1]) for c in changes)
    n_mod = sum(1 for c in changes if c[0] == 'changed')
    n_merge = sum(1 for c in changes if c[0] in ('merged', 'split'))
    n_add = sum(1 for c in changes if c[0] == 'added')
    n_del = sum(1 for c in changes if c[0] == 'removed')
    print('  sentences: %d of %d unchanged; %d changed, %d merged or split, %d added, %d removed%s' % (
        same, len(sa), n_mod, n_merge, n_add, n_del,
        '' if show_changes or not changes else '  (--changes lists them)'))
    if show_changes and changes:
        print('\n== Changed sentences (match each to a rule in the report) ==')
        for k, (kind, olds, news) in enumerate(changes, 1):
            ln = olds[0][0] if olds else (news[0][0] if news else 0)
            print('  C%d [%s] %s line %d' % (k, kind, 'original' if olds else 'revised', ln))
            for _, s in olds:
                print('    - ' + clip(s, 400))
            for _, s in news:
                print('    + ' + clip(s, 400))
    return warn


def audit(D, lex, max_words, max_zh, verbose, base=None):
    print('\n== AI-tell candidates (%s) ==' % os.path.basename(D.path))
    hits = D.lexicon_hits(lex)
    base_hits = base.lexicon_hits(lex) if base else None
    cats = [c for c in lex.kind]
    any_remove = False
    for cat in cats:
        ch = [h for h in hits if h[0] == cat]
        bh = [h for h in base_hits if h[0] == cat] if base_hits is not None else None
        if not ch and not bh:
            continue
        cnt = '%d' % len(ch) if bh is None else '%d -> %d' % (len(bh), len(ch))
        if lex.kind.get(cat) == 'verify':
            words = collections.Counter(h[1] for h in ch)
            print('  [verify] %-22s %s  %s' % (cat, cnt, ', '.join('%s x%d' % kv for kv in words.most_common(12))))
            if verbose:
                for _, w, ln, ctx in ch[:60]:
                    print('      line %d: %s' % (ln, ctx))
            continue
        any_remove = any_remove or bool(ch)
        print('  %-31s %s   (%s)' % (cat, cnt, lex.desc.get(cat, '')))
        for _, w, ln, ctx in ch[:40]:
            print('      line %d: %s' % (ln, ctx))
        if len(ch) > 40:
            print('      ... %d more' % (len(ch) - 40))
    if not any_remove:
        print('  no remove-type candidates')

    print('\n== Evidence placeholders to fill ==')
    if base:
        print('  count %d -> %d' % (len(base.placeholders), len(D.placeholders)))
    for ph, ln in D.placeholders[:60]:
        print('  line %d: %s' % (ln, clip(ph, 100)))
    if not D.placeholders:
        print('  none')

    print('\n== Sentence patterns (candidates; see SKILL.md Rule 4) ==')
    pc = D.pattern_checks()
    bpc = base.pattern_checks() if base else None
    for name, (summary, items) in pc.items():
        if bpc is not None:
            summary = '%s -> %s' % (bpc[name][0].split(' ')[0], summary)
        print('  %-58s %s' % (name, summary))
        for ln, txt in items[:15]:
            print('      line %d: %s' % (ln, txt))
        if len(items) > 15:
            print('      ... %d more' % (len(items) - 15))

    print('\n== Dashes used as punctuation ==')
    dh = D.dash_hits()
    if base:
        print('  count %d -> %d' % (len(base.dash_hits()), len(dh)))
    for name, ln, ctx in dh[:40]:
        print('  line %d [%s]: %s' % (ln, name, ctx))
    if not dh:
        print('  none')

    print('\n== Sentences ==')
    sents = D.sentences()
    unit = 'characters' if D.chinese else 'words'

    def size(s):
        return len(re.sub(r'\s', '', s)) if D.chinese else len(s.split())

    lim = max_zh if D.chinese else max_words
    body_sents = [x for x in sents if not x[2].startswith(TITLE)]
    longs = [x for x in body_sents if size(x[2]) > lim]
    if base:
        b_longs = [x for x in base.sentences() if not x[2].startswith(TITLE) and
                   (len(re.sub(r'\s', '', x[2])) if base.chinese else len(x[2].split())) > lim]
        print('  over %d %s: %d -> %d' % (lim, unit, len(b_longs), len(longs)))
    else:
        print('  over %d %s: %d of %d sentences' % (lim, unit, len(longs), len(body_sents)))
    for _, ln, s in longs[:30]:
        print('      line %d (%d %s): %s' % (ln, size(s), unit, clip(s, 100)))
    if not D.chinese:
        runs, run = [], []
        prev_para = None
        for p, ln, s in sents:
            short = (not s.startswith(TITLE)) and MPH not in s and len(s.split()) < 9
            if short and (prev_para is None or p == prev_para):
                run.append((ln, s))
            else:
                if len(run) >= 3:
                    runs.append(run)
                run = [(ln, s)] if short else []
            prev_para = p
        if len(run) >= 3:
            runs.append(run)
        print('  runs of 3+ sentences under 9 words: %d' % len(runs))
        for r in runs[:15]:
            print('      line %d: %s' % (r[0][0], clip(' | '.join(s for _, s in r), 110)))
        stacks = []
        for (p1, ln1, s1), (p2, _, s2) in zip(sents, sents[1:]):
            if p1 == p2 and ADDITIVE.match(s1) and ADDITIVE.match(s2):
                stacks.append((ln1, s1, s2))
        print('  consecutive sentences opening with additive connectives: %d' % len(stacks))
        for ln, s1, s2 in stacks[:15]:
            print('      line %d: %s | %s' % (ln, clip(s1, 50), clip(s2, 50)))

    rows, results, has_app = D.structure()
    if rows or results:
        print('\n== Structure ==')
        if rows:
            main = [r for r in rows if not r[3]]
            top = min(r[0] for r in rows)
            n_top_main = sum(1 for r in main if r[0] == top)
            print('  top-level headings in main text: %d%s' % (
                n_top_main, (', appendix: %d' % sum(1 for r in rows if r[3] and r[0] == top)) if has_app else ''))
            for idx, (lvl, title, ln, in_app) in enumerate(rows):
                kids = []
                for lvl2, title2, ln2, _ in rows[idx + 1:]:
                    if lvl2 <= lvl:
                        break
                    if lvl2 == lvl + 1:
                        kids.append(title2)
                if len(kids) == 1:
                    print('  ONE CHILD: "%s" (line %d) has a single subdivision "%s"' % (
                        clip(title, 50), ln, clip(kids[0], 50)))
        if results:
            main_r = {k[1]: v for k, v in results.items() if k[0] == 'main'}
            app_r = {k[1]: v for k, v in results.items() if k[0] == 'appendix'}
            print('  formal environments, main text: %s' % (main_r or '{}'))
            if app_r:
                print('  formal environments, appendix:  %s' % app_r)
            n_res = sum(v for k, v in main_r.items() if k in RESULT_ENVS)
            print('  numbered results in main text (theorem/proposition/lemma/corollary): %d' % n_res)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('mode', choices=['audit', 'compare'])
    ap.add_argument('files', nargs='+')
    ap.add_argument('--lexicon', default=DEFAULT_LEXICON)
    ap.add_argument('--max-words', type=int, default=35)
    ap.add_argument('--max-zh-chars', type=int, default=90)
    ap.add_argument('--verbose', action='store_true', help='list every verify-type hit')
    ap.add_argument('--changes', action='store_true', help='compare: print every changed sentence')
    a = ap.parse_args()
    lex = Lexicon(a.lexicon)
    if a.mode == 'audit':
        if len(a.files) != 1:
            ap.error('audit takes one file')
        D = Doc(a.files[0])
        print('file: %s  (%s%s)' % (a.files[0], 'LaTeX' if D.latex else 'Markdown' if D.markdown else 'plain text',
                                   ', Chinese' if D.chinese else ''))
        audit(D, lex, a.max_words, a.max_zh_chars, a.verbose)
        return 0
    if len(a.files) != 2:
        ap.error('compare takes ORIGINAL REVISED')
    A, B = Doc(a.files[0]), Doc(a.files[1])
    print('original: %s\nrevised:  %s' % tuple(a.files))
    print('\n== Invariants (must be unchanged unless the change is intended and reported) ==')
    ok = True
    ok &= print_counter_diff('numbers', A.numbers, B.numbers)
    ok &= print_counter_diff('citations', A.cites, B.cites, show_ctx=False)
    if A.latex or B.latex or A.refs or B.refs:
        ok &= print_counter_diff('cross-references and labels', A.refs, B.refs, show_ctx=False)
    ok &= compare_math(A, B)
    if A.latex or B.latex:
        ok &= compare_formal(A, B)
        if A.preamble is not None or B.preamble is not None:
            same = (A.preamble or '') == (B.preamble or '')
            print('  %-34s %s' % ('preamble', 'unchanged' if same else 'CHANGED'))
            ok &= same
    print('\n  RESULT: %s' % ('all invariants hold' if ok else
                             'differences found; revert each unintended one and list intended ones in the report'))
    w = conservation(A, B, a.changes)
    if w:
        print('\n  %d conservation warning group(s): check that each listed item is intended' % w)
    audit(B, lex, a.max_words, a.max_zh_chars, a.verbose, base=A)
    return 0 if ok else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
