{ pkgs ? import <nixpkgs> {} }:
let
  pythonWPkgs = pkgs.python3.withPackages (p: with p; [
    #ctypes
    pyserial
    tkinter
  ]);
  vscodeIncludePath = pkgs.writeText "vscode-includepath.json" (builtins.toJSON [
    "${pkgs.glibc.dev}/include"
	  "${pkgs.gcc-unwrapped}/include/c++/${pkgs.gcc-unwrapped.version}/"
	  "${pkgs.gcc-unwrapped}/include/c++/${pkgs.gcc-unwrapped.version}/${pkgs.stdenv.buildPlatform.config}/"
  ]);
  printVscodeIncludePath = pkgs.writeShellScriptBin "vscode-includepath" ''
    ${pkgs.jq}/bin/jq <${vscodeIncludePath}
  '';
in
pkgs.mkShell {
  packages = with pkgs; [ gcc gnumake pythonWPkgs printVscodeIncludePath gdb ];
}
