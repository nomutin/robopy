# Getting Started

インストールから実行まで、ROSやその他の依存関係をインストールする必要はありません.  
環境や使用しているパッケージマネージャに合わせてインストール方法を選択してください.

## with Package Manager <small>(recommended)</small>

パッケージ管理ツールを使用するのが無難です.  
メジャーなツールはgithubからのビルドをサポートしているため、それらを使いましょう.

=== "pipenv"

    ``` sh
    pipenv install git+https://github.com/keio-crl/robopy.git
    ```

=== "poetry"

    ``` sh
    poetry add git+https://github.com/keio-crl/robopy.git
    ```

=== "rye"

    ``` sh
    rye add robopy --git+https://github.com/keio-crl/robopy.git
    ```

!!! tip

    pipenv はイマイチ（pyproject.tomlベースではなくlockも遅い）なので、
    他のパッケージマネージャを使うことをお勧めします.

## with pip

ロボット用のPCなど、仮想環境を使いたくない場合はpipを使ってインストールしてください.

    pip install git+https://github.com/keio-crl/robopy.git

## with git

もし Robopy の機能をいじりたい場合は、ソースコードを直接いじるのもいいでしょう.  
詳細な仕様については [API Document](api.md) を参照してください.
[Issue](https://github.com/keio-crl/robopy/issues) や [Pull Request](https://github.com/keio-crl/robopy/pulls) は大歓迎です.

    git clone https://github.com/keio-crl/robopy.git 