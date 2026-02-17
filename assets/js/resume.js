function showResume(type) {
  const short = document.getElementById("resume-short");
  const long = document.getElementById("resume-long");
  const download = document.getElementById("download");

  const short_btn = document.getElementById("short-btn");
  const long_btn = document.getElementById("long-btn");
  const down_btn = document.getElementById("down-btn");

  if (type === "short") {
    short.style.display = "block";
    long.style.display = "none";
    download.style.display = "none";
    short_btn.classList.add("active");
    long_btn.classList.remove("active");
    down_btn.classList.remove("active");
  } else if (type === "long") {
    short.style.display = "none";
    long.style.display = "block";
    download.style.display = "none";
    short_btn.classList.remove("active");
    long_btn.classList.add("active");
    down_btn.classList.remove("active");
  } else {
    short.style.display = "none";
    long.style.display = "none";
    download.style.display = "block";
    short_btn.classList.remove("active");
    long_btn.classList.remove("active");
    down_btn.classList.add("active");
  }
}
