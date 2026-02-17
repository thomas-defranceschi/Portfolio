function showResume(type) {
  const short = document.getElementById("resume-short");
  const long = document.getElementById("resume-long");
  const download = document.getElementById("download");

  if (type === "short") {
    short.style.display = "block";
    long.style.display = "none";
    download.style.display = "none"
  } else if (type === "long") {
    short.style.display = "none";
    long.style.display = "block";
    download.style.display = "none";
  } else {
    short.style.display = "none";
    long.style.display = "none";
    download.style.display = "block";
  }
}
