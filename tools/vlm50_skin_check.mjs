// Task 50 — VLM-верификация локального бэкапа картинки #51 (196411):
// есть ли зеркальный (повёрнутый не в ту сторону) текст «СССР» на модели скина.
// SDK z-ai-web-dev-sdk createVision, image_url = data:base64 (паттерн док 36 / stream-чанки).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const SRC = '/home/z/my-project/output/evidence_post/forumcdn_196411_n51_image_20261014_1315.png';
const OUT_TXT = '/home/z/my-project/output/evidence_post/vlm_n51_skin_check_20261014_1545.txt';

const b64 = fs.readFileSync(SRC).toString('base64');

const PROMPT = `Опиши изображение строго по тому, что видно. Структура ответа:
1. ЧТО НА ИЗОБРАЖЕНИИ — общий состав (персонаж, модель, скафандр/броня, элементы UI и т.п.).
2. ВСЕ ТЕКСТЫ/НАДПИСИ, которые видны, дословно (кириллица/латиница).
3. Есть ли надпись «СССР» на модели (наплечник/пластина/ткань)? Как она РАЗПОЛОЖЕНА и ЧИТАЕТСЯ: нормально слева направо или ЗЕРКАЛЬНО (символы обращены в обратную сторону, как отражение в зеркале)? Объясни, по каким признакам ты это определил(а).
4. Советская символика: флаг, серп и молот, звезда — что именно видно и на каких элементах модели.
5. Прочие детали (интерфейс игры, курсор, кнопки, фон).
Не домысливай за пределы картинки; если чего-то не видно — так и напиши.`;

const zai = await ZAI.create();
let res, raw = '';
try {
  res = await zai.chat.completions.createVision({
    model: 'glm-4.5v',
    thinking: { type: 'disabled' },
    messages: [
      { role: 'system', content: 'Ты — точный аналитик изображений. Отвечай по-русски, структурно, строго по изображению.' },
      { role: 'user', content: [
        { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } },
        { type: 'text', text: PROMPT },
      ]},
    ],
  });
  raw = res?.choices?.[0]?.message?.content ?? JSON.stringify(res, null, 2);
} catch (e) {
  raw = 'VLM_ERROR: ' + (e?.message ?? String(e));
  console.error(raw);
}

const header = [
  'VLM SKIN CHECK — forumcdn_196411_n51_image_20261014_1315.png',
  'Задача: верификация утверждения автора — «на картинке ошибка модели скина, текст СССР повёрнут не в ту сторону»',
  'Время: ' + new Date().toISOString(),
  'Файл: PNG 448x344, sha256 6eec7f699fecf915dcdd6f47afb96c8afd180ce366bd27b21489ef904f68189e (канон Task 48)',
  'Метод: z-ai-web-dev-sdk createVision, model glm-4.5v, image_url data:base64',
  'Ограничение: VLM-вывод ≠ истина; первичный источник — глаза автора (§2.9: видно ≠ атрибутируется)',
  '---',
  '',
].join('\n');

fs.writeFileSync(OUT_TXT, header + raw + '\n');
console.log('SAVED:', OUT_TXT);
console.log('---VLM ANSWER---');
console.log(raw);
