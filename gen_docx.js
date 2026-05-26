const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageBreak, PageNumber
} = require('docx');

const data = JSON.parse(fs.readFileSync('/workspace/kids_vocab/vocabulary.json', 'utf-8'));
const words = data.words;
const books = data.books;

// 按书分组
const byBook = {};
books.forEach(b => { byBook[b.title] = { ...b, words: [] }; });
words.forEach(w => {
  (w.books || []).forEach(bookTitle => {
    if (byBook[bookTitle]) {
      byBook[bookTitle].words.push(w);
    }
  });
});

const border = { style: BorderStyle.SINGLE, size: 1, color: "DDDDDD" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

// 正文段落
function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    ...opts,
    children: [new TextRun({ text, font: "Microsoft YaHei", size: 22, ...opts.run })],
  });
}

// 标题
function heading(text, level) {
  return new Paragraph({
    heading: level,
    spacing: { before: level === HeadingLevel.HEADING_1 ? 400 : 280, after: 200 },
    children: [new TextRun({ text, font: "Arial", bold: true, size: level === HeadingLevel.HEADING_1 ? 36 : 30 })],
  });
}

// 单个词汇行：序号 | 单词 | 词性 | 中文释义 | 例句
function wordRow(idx, wordEntry) {
  const { word, pos, meaning, examples } = wordEntry;
  const exText = (examples && examples.length > 0) ? examples.join(' | ') : '—';
  
  return new TableRow({
    children: [
      makeCell(`${idx}`, 600, "center"),
      makeCell(word, 1600, "left", true),
      makeCell(pos || '—', 800, "center"),
      makeCell(meaning, 2000, "left"),
      makeCell(exText, 3360, "left"),
    ],
  });
}

function makeCell(text, width, align, bold = false) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    margins: cellMargins,
    shading: bold ? { fill: "F5F0FF", type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({
      alignment: align === "center" ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: [new TextRun({
        text: String(text),
        font: "Arial",
        size: 19,
        bold: bold,
      })],
    })],
  });
}

function headerRow() {
  const hdrStyle = { fill: "6C5CE7", type: ShadingType.CLEAR };
  const hdrBorders = {
    top: { style: BorderStyle.SINGLE, size: 1, color: "6C5CE7" },
    bottom: { style: BorderStyle.SINGLE, size: 2, color: "6C5CE7" },
    left: { style: BorderStyle.SINGLE, size: 1, color: "6C5CE7" },
    right: { style: BorderStyle.SINGLE, size: 1, color: "6C5CE7" },
  };
  const hdrRun = { font: "Arial", size: 20, bold: true, color: "FFFFFF" };
  const cols = [
    { text: "#", w: 600 },
    { text: "单词 Word", w: 1600 },
    { text: "词性", w: 800 },
    { text: "中文释义", w: 2000 },
    { text: "例句 Example", w: 3360 },
  ];
  return new TableRow({
    tableHeader: true,
    children: cols.map(c => new TableCell({
      borders: hdrBorders,
      width: { size: c.w, type: WidthType.DXA },
      margins: cellMargins,
      shading: hdrStyle,
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: c.text, ...hdrRun })],
      })],
    })),
  });
}

// 构建文档
const children = [];

// 封面
children.push(new Paragraph({ spacing: { before: 3000 } }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "🐻 小朋友英语词汇本", font: "Arial", size: 56, bold: true, color: "6C5CE7" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 200 },
  children: [new TextRun({ text: "斯伯恩自然拼读分级读物", font: "Microsoft YaHei", size: 32, color: "888888" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 400 },
  children: [new TextRun({ text: `共 ${data.total} 个词汇 · ${data.books.length} 本书`, font: "Microsoft YaHei", size: 26, color: "AAAAAA" })],
}));
children.push(new Paragraph({ children: [new PageBreak()] }));

// 每本书一个章节
books.forEach((book, bookIdx) => {
  const bookWords = byBook[book.title].words;
  
  children.push(heading(`${book.title}`, HeadingLevel.HEADING_1));
  children.push(new Paragraph({
    spacing: { after: 240 },
    children: [new TextRun({ text: `📖 ${book.cn}  |  ${bookWords.length} 个词汇`, font: "Microsoft YaHei", size: 22, color: "888888" })],
  }));

  // 词汇表
  const tableRows = [headerRow()];
  bookWords.forEach((w, i) => {
    tableRows.push(wordRow(i + 1, w));
  });

  children.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [600, 1600, 800, 2000, 4360],
    rows: tableRows,
  }));

  children.push(new Paragraph({ spacing: { after: 200 } }));

  // 除了最后一本，加分隔
  if (bookIdx < books.length - 1) {
    children.push(new Paragraph({ children: [new PageBreak()] }));
  }
});

// 词汇索引（全部词汇字母排序）
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(heading("附录：全部词汇索引", HeadingLevel.HEADING_1));
children.push(new Paragraph({
  spacing: { after: 240 },
  children: [new TextRun({ text: `按字母排序，共 ${data.total} 个词汇`, font: "Microsoft YaHei", size: 22, color: "888888" })],
}));

const sorted = [...words].sort((a, b) => a.word.localeCompare(b.word));
const idxRows = [headerRow()];
sorted.forEach((w, i) => idxRows.push(wordRow(i + 1, w)));

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [600, 1600, 800, 2000, 4360],
  rows: idxRows,
}));

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1200, right: 1200, bottom: 1200, left: 1200 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "🐻 小朋友英语词汇本", font: "Arial", size: 18, color: "BBBBBB" })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "第 ", font: "Arial", size: 18, color: "BBBBBB" }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "BBBBBB" }),
            new TextRun({ text: " 页", font: "Arial", size: 18, color: "BBBBBB" }),
          ],
        })],
      }),
    },
    children,
  }],
});

const outPath = '/workspace/kids_vocab/小朋友英语词汇本.docx';
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log(`✅ 已生成: ${outPath}`);
  console.log(`   共 ${data.total} 个词汇，${data.books.length} 本书 + 索引`);
}).catch(err => {
  console.error('❌', err);
});
