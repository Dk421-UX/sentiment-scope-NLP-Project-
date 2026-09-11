const limit = 10000;
const input = document.querySelector('#textInput');
const count = document.querySelector('#characterCount');
const error = document.querySelector('#inputError');
const button = document.querySelector('#analyzeButton');
const statusBox = document.querySelector('#status');
const results = document.querySelector('#results');

function updateCount() {
  const length = input.value.length;
  count.textContent = `${length.toLocaleString()} / 10,000`;
  count.style.color = length === limit ? '#ffbf5b' : '';
  error.textContent = length > limit ? 'Text is over the limit.' : '';
}

function addText(parent, text, className = '') {
  const node = document.createElement('span');
  node.textContent = text;
  node.className = className;
  parent.append(node);
}

function chips(id, items, type) {
  const holder = document.querySelector(id); holder.replaceChildren();
  if (!items.length) return addText(holder, 'No matching terms.', 'empty');
  items.forEach(item => {
    const note = [item.negated_by && `negated by ${item.negated_by}`, item.intensified_by && `boosted by ${item.intensified_by}`].filter(Boolean).join(', ');
    addText(holder, `${item.word} (${item.score > 0 ? '+' : ''}${item.score})${note ? ` · ${note}` : ''}`, `chip ${type}`);
  });
}

function render(data) {
  results.hidden = false;
  document.querySelector('#sentimentLabel').textContent = data.sentiment;
  document.querySelector('#scoreValue').textContent = data.score.toFixed(2);
  document.querySelector('#explanation').textContent = data.explanation;
  document.querySelector('#mixedNotice').hidden = !data.mixed_sentiment;
  const metrics = [['Characters',data.character_count],['Words',data.word_count],['Sentences',data.sentence_count],['Positive terms',data.positive_words.length],['Negative terms',data.negative_words.length],['Neutral tokens',data.neutral_token_count]];
  const metricBox = document.querySelector('#metrics'); metricBox.replaceChildren();
  metrics.forEach(([name,value]) => { const el=document.createElement('div');el.className='metric';el.innerHTML=`<b>${value}</b><span>${name}</span>`;metricBox.append(el); });
  const total = data.positive_score + data.negative_score || 1;
  const rows = [['Positive',data.positive_score,'#48c99b'],['Negative',data.negative_score,'#ff6e82'],['Net raw',data.raw_score,'#5d8cff']];
  const breakdown=document.querySelector('#breakdown');breakdown.replaceChildren();
  rows.forEach(([name,value,color])=>{const row=document.createElement('div');row.className='break-row';row.innerHTML=`<span>${name}</span><div class="bar"><i style="width:${Math.min(Math.abs(value)/total*100,100)}%;background:${color}"></i></div><b>${value.toFixed(2)}</b>`;breakdown.append(row)});
  const details=document.querySelector('#ruleDetails');details.replaceChildren();
  addText(details, `Strength: ${data.sentiment_strength}. Raw score: ${data.raw_score}; normalized score: ${data.score}.`, '');
  if(data.negations.length) addText(details, `Negations detected: ${data.negations.join(', ')}.`, '');
  if(data.intensifiers.length) addText(details, `Intensifiers detected: ${data.intensifiers.join(', ')}.`, '');
  chips('#positiveChips', data.positive_contributors, 'positive'); chips('#negativeChips', data.negative_contributors, 'negative');
}

async function analyze() {
  const text=input.value;
  if (!text.trim()) { error.textContent='Enter some text before analyzing.'; input.focus(); return; }
  if (text.length > limit) { error.textContent='Text is over the limit.'; return; }
  error.textContent=''; statusBox.textContent='Analyzing locally…'; statusBox.className='status'; button.disabled=true;
  try { const response=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})}); const data=await response.json(); if(!response.ok) throw new Error(data.error || 'Analysis failed.'); render(data); statusBox.textContent='Analysis complete.'; }
  catch (err) { statusBox.textContent=err.message || 'Unable to analyze the text.'; statusBox.className='status error'; }
  finally { button.disabled=false; }
}
input.addEventListener('input', updateCount); button.addEventListener('click', analyze);
document.querySelector('#resetButton').addEventListener('click',()=>{input.value='';updateCount();error.textContent='';statusBox.textContent='';results.hidden=true;input.focus()}); updateCount();
