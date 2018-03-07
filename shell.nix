with import <nixpkgs> { };
let
  ffmpeg-with-fdkaac = ffmpeg-full.override { nonfreeLicensing = true; fdkaacExtlib = true; };
in
  runCommand "dummy" { buildInputs = [ python35Full ffmpeg-with-fdkaac ]; } ""
