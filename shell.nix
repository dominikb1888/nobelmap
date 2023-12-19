{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = with pkgs.python311Packages; [
    poetry-core
    ipython
    jupyterlab

    pytest
    requests
    python-dotenv
    fastapi
    uvicorn

    (buildPythonPackage {
      pname = "sqlmodel";
      version = "0.0.14";
      src = fetchPypi {
        inherit pname version;
        sha256 = "0bff8fc94af86b44925aa813f56cf6aabdd7f156b73259f2f60692c6a64ac90e";
      };
      propagatedBuildInputs = [
      ];
    })

  ];

in pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    pythonEnv
    # keep this line if you use bash
    # pkgs.bashInteractive
  ];
}
