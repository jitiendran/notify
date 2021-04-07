const popup = document.querySelector(".pop-up");

const close = document.getElementById("close");

const openPopup = () => {
  popup.style.display = "flex";
};

close.addEventListener("click", () => {
  popup.style.display = "none";
});
