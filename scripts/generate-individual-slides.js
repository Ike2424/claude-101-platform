import fs from 'fs';
import path from 'path';

// Mapa de lecciones: id -> { modulo, leccion, slide_num }
const LESSONS = [
  { id: 'l1-1', file: 'L1-1-slides.html', slide: 1 },
  { id: 'l1-2', file: 'L1-2-slides.html', slide: 2 },
  { id: 'l1-3', file: 'L1-3-slides.html', slide: 3 },
  { id: 'l1-4', file: 'L1-4-slides.html', slide: 4 },
  { id: 'l2-1', file: 'L2-1-slides.html', slide: 5 },
  { id: 'l2-2', file: 'L2-2-slides.html', slide: 6 },
  { id: 'l2-3', file: 'L2-3-slides.html', slide: 7 },
  { id: 'l3-1', file: 'L3-1-slides.html', slide: 8 },
  { id: 'l3-2', file: 'L3-2-slides.html', slide: 9 },
  { id: 'l3-3', file: 'L3-3-slides.html', slide: 10 },
  { id: 'l4-1', file: 'L4-1-slides.html', slide: 11 },
  { id: 'l4-2', file: 'L4-2-slides.html', slide: 12 },
  { id: 'l4-3', file: 'L4-3-slides.html', slide: 13 },
  { id: 'l4-4', file: 'L4-4-slides.html', slide: 14 },
  { id: 'l5-1', file: 'L5-1-slides.html', slide: 15 },
  { id: 'l5-2', file: 'L5-2-slides.html', slide: 16 },
  { id: 'l5-3', file: 'L5-3-slides.html', slide: 17 },
  { id: 'l6-1', file: 'L6-1-slides.html', slide: 18 },
  { id: 'l6-2', file: 'L6-2-slides.html', slide: 19 },
  { id: 'l6-3', file: 'L6-3-slides.html', slide: 20 },
  { id: 'l7-1', file: 'L7-1-slides.html', slide: 21 },
  { id: 'l7-2', file: 'L7-2-slides.html', slide: 22 },
  { id: 'l7-3', file: 'L7-3-slides.html', slide: 23 },
  { id: 'l7-4', file: 'L7-4-slides.html', slide: 24 },
  { id: 'l8-1', file: 'L8-1-slides.html', slide: 25 },
  { id: 'l8-2', file: 'L8-2-slides.html', slide: 26 },
  { id: 'l8-3', file: 'L8-3-slides.html', slide: 27 },
  { id: 'l8-4', file: 'L8-4-slides.html', slide: 28 },
  { id: 'l9-1', file: 'L9-1-slides.html', slide: 29 },
  { id: 'l9-2', file: 'L9-2-slides.html', slide: 30 },
  { id: 'l9-3', file: 'L9-3-slides.html', slide: 31 },
  { id: 'l9-4', file: 'L9-4-slides.html', slide: 32 },
  { id: 'l9-5', file: 'L9-5-slides.html', slide: 33 },
  { id: 'l9-6', file: 'L9-6-slides.html', slide: 34 },
];

// Leer ALL-LESSONS-slides.html
const sourceFile = './public/claude-101-videos/ALL-LESSONS-slides.html';
const content = fs.readFileSync(sourceFile, 'utf8');

// Para cada lección, crear un wrapper HTML que muestra solo ese slide
LESSONS.forEach(lesson => {
  const wrapper = `<!DOCTYPE html>
<html lang="es">
<head>
<!-- Google Analytics 4 -->
<script src="/ga.js"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Claude 101 · Lección ${lesson.file}</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/favicon.svg">
<style>
body { margin: 0; padding: 0; overflow: hidden; }
iframe { width: 100%; height: 100vh; border: none; }
</style>
</head>
<body>
<iframe src="/claude-101-videos/ALL-LESSONS-slides.html?slide=${lesson.slide}" allowfullscreen></iframe>
<script>
  const params = new URLSearchParams(window.location.search);
  const slide = params.get('slide') || ${lesson.slide};
  document.querySelector('iframe').src = '/claude-101-videos/ALL-LESSONS-slides.html?slide=' + slide;
</script>
</body>
</html>`;

  const outputPath = `./public/claude-101-videos/${lesson.file}`;
  fs.writeFileSync(outputPath, wrapper);
  console.log(`✓ Created ${lesson.file}`);
});

console.log(`\n✓ Generated ${LESSONS.length} individual slide files`);
