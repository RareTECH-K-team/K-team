/* スクロール処理 */

const element = document.getElementById("message-area");
const offset = (16 * window.innerHeight) / 100;
const elementBottom = element.getBoundingClientRect().bottom;

window.scrollBy({
    top: elementBottom - window.innerHeight + offset,
    behavior: "auto",
});