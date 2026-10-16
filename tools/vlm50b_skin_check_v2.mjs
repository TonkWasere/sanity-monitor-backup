// Task 50 постфактум 2 — VLM-проба v2: нейтральный сфокусированный промпт
// о направлении строки на нашивке (без наводки на «зеркальность»).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const SRC = '/home/z/my-project/output/evidence_post/forumcdn_196411_n51_image_20261014_1315.png';
const OUT = '/home/z/my-project/output/evidence_post/vlm_n51_skin_check_v2_20261014_1555.txt';

const b64 = fs.readFileSync(SRC).toString('base64');

const PROMPT = `Смотри на красную прямоугольную нашивку на наплечнике персонажа.
1. Перепиши ДОСЛОВНО все текстовые надписи на этой нашивке, символ за символом, в том порядке, как они физически расположены на нашивке СЛЕВА НАПРАВО.
2. Укажи для каждой надписи: какой символ оказался самым ЛЕВЫМ и какой самым ПРАВЫМ на нашивке.
3. Опиши начертание каждой буквы этой надписи: в какую сторону направлена «ножка» буквы Р; выпуклость каждой буквы С (влево или вправо).
4. Есть ли на модели другие текстовые надписи (ремни, пластины, грудь)? Если есть — сделай с ними то же самое.
5. Итог: если бы читатель читал эту надпись как обычный русский текст, получилось бы осмысленное слово «СССР», или что-то другое?`;

const zai = await ZAI.create();
let raw = '';
try {
  const res = await zai.chat.completions.createVision({
    model: 'glm-4.5v',
    thinking: { type: 'disabled' },
    messages: [
      { role: 'system', content: 'Ты — точный аналитик изображений. Отвечай по-русски, строго по изображению, посимвольно. Если не уверен — скажи об этом прямо.' },
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
  'VLM SKIN CHECK v2 — forumcdn_196411_n51_image_20261014_1315.png',
  'Контекст: автор подтвердил, что надпись на нашивке идёт СПРАВА-НАЛЕВО (вместо слева-направо).',
  'Проба v2: нейтральный посимвольный промпт БЕЗ слова «зеркально» (анти-наводка).',
  'Время: ' + new Date().toISOString(),
  'Проба v1 (15:45): VLM прочла «нормально» — расхождение с автором зафиксировано (vlm_n51_skin_check_20261014_1545.txt).',
  '---',
  '',
].join('\n');

fs.writeFileSync(OUT, header + raw + '\n');
console.log('SAVED:', OUT);
console.log('---VLM v2---');
console.log(raw);
