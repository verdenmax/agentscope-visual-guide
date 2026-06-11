import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import i18n  # noqa: E402


class TestInline(unittest.TestCase):
    def test_esc_escapes_html_and_quotes(self):
        self.assertEqual(
            i18n.esc('<a href="x">&'),
            "&lt;a href=&quot;x&quot;&gt;&amp;",
        )

    def test_t_emits_both_lang_spans_in_order(self):
        self.assertEqual(
            i18n.t("中文", "English"),
            '<span lang="zh">中文</span><span lang="en">English</span>',
        )

    def test_p_emits_paired_paragraphs(self):
        self.assertEqual(
            i18n.p("你好", "Hi"),
            '<p lang="zh">你好</p><p lang="en">Hi</p>',
        )

    def test_h2_pair(self):
        self.assertEqual(
            i18n.h2("标题", "Title"),
            '<h2 lang="zh">标题</h2><h2 lang="en">Title</h2>',
        )

    def test_h3_pair(self):
        self.assertEqual(
            i18n.h3("小标题", "Sub"),
            '<h3 lang="zh">小标题</h3><h3 lang="en">Sub</h3>',
        )

    def test_lead_has_lead_class(self):
        out = i18n.lead("引言", "Lead")
        self.assertIn('<p class="lead" lang="zh">引言</p>', out)
        self.assertIn('<p class="lead" lang="en">Lead</p>', out)


class TestCard(unittest.TestCase):
    def test_card_default_note_tag_bilingual(self):
        out = i18n.card("正文", "Body")
        self.assertIn('<div class="card note">', out)
        self.assertIn('<span lang="zh">📌 注意</span>', out)
        self.assertIn('<span lang="en">📌 Note</span>', out)
        self.assertIn('<div lang="zh">正文</div>', out)
        self.assertIn('<div lang="en">Body</div>', out)

    def test_card_analogy_kind(self):
        out = i18n.card("比喻", "Metaphor", kind="analogy")
        self.assertIn('<div class="card analogy">', out)
        self.assertIn("🧩 生活类比", out)

    def test_card_custom_tag(self):
        out = i18n.card("a", "b", kind="tip", tag_zh="自定义", tag_en="Custom")
        self.assertIn("自定义", out)
        self.assertIn("Custom", out)


class TestTable(unittest.TestCase):
    def test_table_headers_and_rows_bilingual(self):
        out = i18n.table(
            [("痛点", "Pain"), ("做法", "Approach")],
            [[("锁定", "Lock-in"), ("统一接口", "Unified API")]],
        )
        self.assertIn('<table class="t">', out)
        self.assertIn("<th><span lang=\"zh\">痛点</span>"
                      "<span lang=\"en\">Pain</span></th>", out)
        self.assertIn("<td><span lang=\"zh\">锁定</span>"
                      "<span lang=\"en\">Lock-in</span></td>", out)


class TestCode(unittest.TestCase):
    def test_python_keyword_highlighted(self):
        out = i18n.code("from x import y")
        self.assertIn('<span class="kw">from</span>', out)
        self.assertIn('<span class="kw">import</span>', out)
        self.assertIn('<pre class="code"', out)

    def test_python_string_and_comment_highlighted(self):
        out = i18n.code('x = "hi"  # note')
        self.assertIn('<span class="st">&quot;hi&quot;</span>', out)
        self.assertIn('<span class="cm"># note</span>', out)

    def test_keyword_inside_string_not_highlighted(self):
        out = i18n.code('x = "def import"')
        self.assertNotIn('<span class="kw">def</span>', out)
        self.assertIn('<span class="st">&quot;def import&quot;</span>', out)

    def test_unparseable_falls_back_to_escaped(self):
        out = i18n.code("agent = Agent(  # missing close")
        self.assertIn("Agent(", out)
        self.assertIn('<pre class="code"', out)

    def test_non_python_escaped_only(self):
        out = i18n.code("rm -rf <dir>", lang="bash")
        self.assertIn("rm -rf &lt;dir&gt;", out)
        self.assertNotIn('class="kw"', out)

    def test_caption_bilingual(self):
        out = i18n.code("x = 1", cap_zh="赋值", cap_en="Assign")
        self.assertIn('<figure class="code-fig">', out)
        self.assertIn('<div class="code-cap" lang="zh">赋值</div>', out)
        self.assertIn('<div class="code-cap" lang="en">Assign</div>', out)


class TestAccordion(unittest.TestCase):
    def test_accordion_structure_bilingual(self):
        out = i18n.accordion("标题", "Title", "<p>body</p>", num=2)
        self.assertIn('<details class="accordion">', out)
        self.assertIn('<span class="badge-num">2</span>', out)
        self.assertIn('<span lang="zh">标题</span>', out)
        self.assertIn('<span lang="en">Title</span>', out)
        self.assertIn('<div class="acc-body"><p>body</p></div>', out)

    def test_accordion_without_num_has_no_badge(self):
        out = i18n.accordion("a", "b", "x")
        self.assertNotIn("badge-num", out)


class TestKeypoints(unittest.TestCase):
    def test_keypoints_list_bilingual(self):
        out = i18n.keypoints([("要点一", "Point 1"), ("要点二", "Point 2")])
        self.assertIn('<div class="keypoints">', out)
        self.assertIn('<li><span lang="zh">要点一</span>'
                      '<span lang="en">Point 1</span></li>', out)
        self.assertIn("关键要点", out)
        self.assertIn("Key takeaways", out)


class TestConvenience(unittest.TestCase):
    def test_analogy_note_tip_important_delegate(self):
        self.assertIn('class="card analogy"', i18n.analogy("a", "b"))
        self.assertIn('class="card note"', i18n.note("a", "b"))
        self.assertIn('class="card tip"', i18n.tip("a", "b"))
        self.assertIn('class="card important"', i18n.important("a", "b"))

    def test_highlight_has_design_highlight_tag(self):
        out = i18n.highlight("精妙", "Elegant")
        self.assertIn("💡 设计亮点", out)
        self.assertIn("💡 Design highlight", out)

    def test_blocks_joins_parts(self):
        self.assertEqual(i18n.blocks("<a>", "<b>", "<c>"), "<a><b><c>")


class TestSourceMap(unittest.TestCase):
    def test_source_map_renders_file_and_desc(self):
        out = i18n.source_map([("agent/_agent.py", "Agent 类", "Agent class")])
        self.assertIn("<code>agent/_agent.py</code>", out)
        self.assertIn('<span lang="zh">Agent 类</span>', out)
        self.assertIn('<span lang="en">Agent class</span>', out)
        self.assertIn("源码对应", out)
