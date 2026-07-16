# markdown_note_fastapi

[README in English](./README.md)

> 本プロジェクトは現在開発中であり、今後も仕様変更や機能追加を行う予定である。

FastAPIを用いて開発しているMarkdown記事管理Web APIである。

ユーザー認証、記事、タグ、コメント、いいねなどの機能を実装している。
保守性を意識し、Router、Service、Repositoryの各レイヤーに責務を分離した構成を採用している。

## 主な機能

* ユーザー登録・認証
* ユーザープロフィールの取得・更新・削除
* Markdown記事の作成・取得・更新・削除
* タグの取得
* コメントの投稿・取得・更新・削除
* 記事へのいいね・いいね解除
* 記事・コメント一覧のページネーション
* 所有者に応じた記事・コメントの更新／削除権限の制御
* `deleted_at` を用いた論理削除


## 設計方針

処理の責務を分離するため、主に以下のレイヤーで構成している。

- **Router**
  - HTTPリクエストの受付
  - リクエストパラメータおよびレスポンスの定義
  - Serviceの呼び出し

- **Service**
  - アプリケーションのユースケースおよびビジネスロジック
  - 権限チェック
  - 複数のRepositoryをまたぐ処理

- **Repository**
  - SQLAlchemyを用いたデータベース操作
  - データの取得・保存・更新・削除

API層、ビジネスロジック、データアクセス処理を分離することで、コードの可読性、保守性、テスト容易性を高めることを目的としている。

## 技術スタック

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT認証

## 環境構築

### 1. リポジトリをクローン

```bash
git clone https://github.com/kikutan-day65/markdown_note_fastapi.git
cd markdown_note_fastapi
```

### 2. 仮想環境を作成・有効化

```bash
python -m venv venv
source venv/bin/activate
```

### 3. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数を設定

プロジェクトのルートディレクトリに `.env` ファイルを作成し、データベース接続情報や認証に必要な値を設定する。

```env
DATABASE_URL=postgresql+psycopg://<username>:<password>@localhost:5432/<database>
SECRET_KEY=<your-secret-key>
```

環境変数名および設定値は、実際のプロジェクト構成に合わせて変更する。

### 5. データベースマイグレーションを実行

```bash
alembic upgrade head
```

### 6. FastAPIを起動

```bash
uvicorn app.main:app --reload
```

### 7. APIドキュメントを確認

起動後、以下のURLからSwagger UIを確認できる。

```text
http://127.0.0.1:8000/docs
```

ReDocは以下のURLから確認できる。

```text
http://127.0.0.1:8000/redoc
```

## 今後の予定

- リフレッシュトークン処理の整備
- テストコードの追加
- エラーハンドリングの整理
- READMEおよびAPI仕様の拡充
- React / TypeScriptを用いたフロントエンドとの連携
- デプロイ環境の構築
