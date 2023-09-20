const addGadget = () => {
  document.getElementById("getGadgets").style.display = "none";
  document.getElementById("uploadGadget").style.display = "block";
};

const getAllGadgets = () => {
  document.getElementById("uploadGadget").style.display = "none";
  document.getElementById("getGadgets").style.display = "flex";
};
