function showResume(type) {
  const short = document.getElementById("resume-short");
  const long = document.getElementById("resume-long");

  if (type === "short") {
    short.style.display = "block";
    long.style.display = "none";
  } else {
    short.style.display = "none";
    long.style.display = "block";
  }
}
