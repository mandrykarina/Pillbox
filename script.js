const addBtn = document.querySelector('.addBtn');
var blockNumber = 2;
addBtn.onclick = () => {
  // Создаем блок и добавляем номер
  const createBlock = document.createElement('div');
  createBlock.className = 'page-block';
  createBlock.innerText = 'Страница ' + blockNumber;
  blockNumber++;
  addBtn.insertAdjacentElement('beforebegin', createBlock);
}