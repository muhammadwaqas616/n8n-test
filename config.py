import os
import time
from typing import NamedTuple

from dotenv import load_dotenv
from pytz import timezone

load_dotenv(override=True)
load_dotenv(dotenv_path="./config.env", override=True)
load_dotenv(dotenv_path="./RELEASE")

# PoC週間TT出力用
EXPAND = False

# docstring記述により、各変数の説明は変数の下部にあることに留意してください。
# VSCodeなどではポップアップで出てきます


class Release(NamedTuple):
    """リリース情報"""

    tag: str
    """コミットについたタグ"""
    commit: str
    """コミットハッシュ"""
    name: str
    """リリース情報として使いやすい総合名"""
    date: str
    """コミット日時"""
    build: str
    """CodeBuild実行日時"""


RELEASE = Release(
    tag=os.getenv("RELEASE_TAG", ""),
    commit=os.getenv("RELEASE_COMMIT", "dev"),
    name=os.getenv("RELEASE", "dev"),
    date=os.getenv("RELEASE_DATE", "dev"),
    build=os.getenv("RELEASE_BUILD", "dev"),
)
"""リリース情報"""

# ディレクトリパス
# メタ設定
EXPORT_EXIT_BUCKET = os.getenv("EXPORT_EXIT_BUCKET", "jins-ap-northeast-1-exportexit-pro")
"""Snowflakeからのデータ取得用のバケット"""

SHIFTAI_INPUT_BUCKET = os.getenv("SHIFTAI_INPUT_BUCKET", "jins-ap-northeast-1-shift-ai-input-pro")
"""外部からの入力バケット"""

SHIFTAI_STORE_BUCKET = os.getenv("SHIFTAI_STORE_BUCKET", "jins-ap-northeast-1-shift-ai-store-pro")
"""内部のみの入出力バケット"""

SHIFTAI_TRACKING_BUCKET = os.getenv("SHIFTAI_TRACKING_BUCKET", "jins-jp-ap-northeast-1-shift-ai-s3-tracking-logs-pro")
"""出力専用のバケット"""

# Snowflakeからのデータ取得用のリポジトリ
FROM_SNOWFLAKE = os.getenv("FROM_SNOWFLAKE", f"s3://{EXPORT_EXIT_BUCKET}/shift_ai/shift_ai-m-R202509-pro")
"""Snowflakeからのデータ取得用のリポジトリ"""

SHIFTAI_INPUT_REPOSITORY = os.getenv("SHIFTAI_INPUT_REPOSITORY", f"s3://{SHIFTAI_INPUT_BUCKET}/R202509")
"""外部からの入力データリポジトリ"""

SHIFTAI_STORE_REPOSITORY = os.getenv("SHIFTAI_STORE_REPOSITORY", f"s3://{SHIFTAI_STORE_BUCKET}/R202509")
"""内部のみの入出力リポジトリ"""

# ## 実入力データ
# 個別に上書き可能です。
WORK_CALENDAR_DATA = os.getenv(
    "WORK_CALENDAR_DATA",
    f"{SHIFTAI_INPUT_REPOSITORY}/?pattern=20%3F%3F/%3F%3F/店舗営業時間_休業日_20%3F%3F%3F%3F.csv*&selector=latest&limit=2",
)
"""外部:店舗個別日付ファイル"""

WORK_TIME_DATA = os.getenv(
    "WORK_TIME_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/config/?pattern=通常営業時間.20%3F%3F%3F%3F%3F%3F.csv*&selector=latest",
)
"""設定:店舗営業時間ファイル"""

WORK_TIME_DEFAULT = os.getenv("WORK_TIME_DEFAULT", "10:00:00-21:00:00")
"""デフォルトの営業時間（非常用）

デフォルトの営業時間を`"09:00:00-15:00:00"`形式で設定することで、店舗営業時間が存在しない場合に設定することができる。
"""

EMP_SKILL_DATA = os.getenv(
    "EMP_SKILL_DATA",
    f"{SHIFTAI_INPUT_REPOSITORY}/?pattern=20%3F%3F/%3F%3F/skill-assign_20%3F%3F%3F%3F%3F%3F.csv*&selector=latest",
)
"""外部:検定情報ファイル（スキルデータレポート）

Talent Paletteからのスキルデータ。csv形式またはxlsx形式。S3はcsv形式想定
"""

WORK_MASTER_DATA = os.getenv(
    "WORK_MASTER_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/config/?pattern=作業マスタ.20%3F%3F%3F%3F%3F%3F.csv*&selector=latest",
)
"""設定:作業マスタファイル"""

COMMON_EVENT_DATA = os.getenv(
    "COMMON_EVENT_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/config/?pattern=全店共通イベント.20%3F%3F%3F%3F%3F%3F.csv*&selector=latest",
)
"""設定:全店共通イベントファイル

時間帯別会計数に一致する期間に合わせた全店共通のイベント情報。"""
# TODO: 内部のrequired-man-hoursに月を含めるべき（当月で複数回出力することがあり得てしまう）
MAN_HOUR_DATA = os.getenv(
    "MAN_HOUR_DATA", f"{SHIFTAI_STORE_REPOSITORY}/?pattern=20%3F%3F/%3F%3F/required-man-hours_*&selector=latest&limit=3"
)
"""内部:必要人時ファイル（必要人時モデル出力）

TT作成対象月の必要人時が必要。
"""

PEAK_DATA = os.getenv(
    "PEAK_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/?pattern=20%3F%3F/%3F%3F/ピークタイム_20%3F%3F%3F%3F.csv*&selector=latest2",
)
"""内部:ピークタイムファイル（必要人時モデル出力）

TT作成対象月のピークタイムが必要。
"""

POS_PRIORITY_DEFAULT_DATA = os.getenv(
    "POS_PRIORITY_DEFAULT_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/priority/?pattern=default.xlsx*&selector=latest",
)
"""設定:ポジション優先度定義ファイル（デフォルト）"""

POS_PRIORITY_PATTERN_DATA = os.getenv(
    "POS_PRIORITY_PATTERN_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/priority/patterns/?pattern=*.xlsx*",
)
"""設定:ポジション優先度定義ファイル（パターン別）"""

POS_PRIORITY_MAP_DATA = os.getenv(
    "POS_PRIORITY_MAP_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/priority/mapping/?pattern=マッピング.xlsx*&selector=latest",
)
"""設定:ポジション優先度マッピングファイル """

# ## API専用データ
HOURLY_SALES_TARGET_DATA = os.getenv(
    "HOURLY_SALES_TARGET_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/?pattern=20%3F%3F/%3F%3F/時間帯別売上予測値_20%3F%3F%3F%3F.csv*&selector=latest2",
)
"""内部:時間帯別売上予測値ファイル

TT作成対象月の時間帯別売上予測値が必要。
"""

SKILLED_POS_DATA = os.getenv(
    "SKILLED_POS_DATA",
    f"{SHIFTAI_STORE_REPOSITORY}/?pattern=20%3F%3F/%3F%3F/skilled-pos_20%3F%3F%3F%3F%3F%3F.csv*&selector=latest",
)
"""内部:希望ポジションファイル

TT作成対象月の希望ポジションが必要。
"""

# ## バッチまたはデバッグ用（API時不要）
SHIFT_DATA = os.getenv("SHIFT_DATA", "./data/input/シフト/")
"""シフトファイル

シフトファイルの入力先は未定（要設定）

TT作成対象月のシフトが必要。設定しない場合は起動しない。
"""

FIXPOS_DATA = os.getenv("FIXPOS_DATA", "./data/input/固定ポジション/")
"""固定ポジションファイル
"""


# 将来的にあった方がいいかも？
SHOP_DATA = os.getenv(
    "SHOP_DATA",
    f"{FROM_SNOWFLAKE}?pattern=%3F%3F%3F%3F-%3F%3F-%3F%3F/dm_rpt_monthly_shift_ai_shop_master_jp.csv*&select=latest",
)
# """店舗マスタファイル"""

UNIQUE_TASK_DATA = os.getenv(
    "UNIQUE_TASK_DATA",
    f"{SHIFTAI_INPUT_REPOSITORY}/?pattern=20%3F%3F/%3F%3F/全店特殊作業_20%3F%3F%3F%3F.csv*&selector=latest2",
)
"""設定:社内特殊作業ファイル

TT作成対象月の連絡事項が必要。
"""

# ## 出力データ（API実行時）
TRANSACTION_TRACKING_LOG_ROOT = os.getenv(
    "TRANSACTION_TRACKING_LOG_ROOT",
    f"s3://{SHIFTAI_TRACKING_BUCKET}/R202509/",
)

# ## 出力データ（バッチ実行時）
TT_OUTPUT = "./data/output"
"""TT出力先（バッチ実行時）"""

# ## レポート出力設定（基本不要だが、ライブラリ一貫性のために設定）
MODEL_NAME = os.getenv("MODEL_NAME", "タイムテーブルモデル")

REPORT_DESTINATION_URI = os.getenv("REPORT_DESTINATION_URI", "stdout://")

FILE_LABELS = {
    "daily_sales_target": "店舗毎日割計画 確定版",
    "shop": "店舗マスタファイル",
    "work_time": "店舗営業時間ファイル",
    "work_calendar": "店舗個別日付ファイル",
    "hourly_performance": "時間帯別会計数",
    "visited": "発券数",
    "history": "シフトファイル",
    "common_event": "全店共通イベントファイル",
    "shop_event": "店舗毎イベントファイル",
    "unique_task": "社内特殊作業ファイル",
}

# ## デバッグ用設定

DONT_SET_ON_PRODUCTION__ENABLE_MODIFY__ = os.getenv("DONT_SET_ON_PRODUCTION__ENABLE_MODIFY__", None)
"""テスト用のコードを埋め込むための条件

データを強引に書き換えたいなどの場合に、if config.DONT_SET_ON_PRODUCTION__ENABLE_MODIFY: で条件分岐することで、
何かの間違いで本番コードを書き換えてしまうことを防ぐ。
"""

# Dataframeのデータを保持するかどうか
DONT_SET_ON_PRODUCTION__KEEP_FOR_DEBUG__ = os.getenv("DONT_SET_ON_PRODUCTION__KEEP_FOR_DEBUG__", None)
"""Dataframeのデータを保持するかどうか

ほとんどの処理ではDataframeは切り詰めてよく、また不要な依存関係を残さないように切り詰めるべきだが、
デバッグ時にはDataframeの内容を保持しておきたい場合がある。
"""

# ## その他
BEGIN = time.time()
"""開始日時

うかつなにnow()をまき散らすと、実行タイミングでひどいことになるので、起動時間を記録。
ここにあるべきかどうかは微妙だが、設定できるとデバッグ時の嬉しさもあるのでひとまずここにおいておく
"""

TZ = timezone("Asia/Tokyo")
"""タイムゾーン設定"""

ENABLE_DATA_VALIDATION = os.getenv("ENABLE_DATA_VALIDATION", "false")
"""データバリデーションを有効にするかどうか"""

FIXED_POSITION_SHOP_CODES = [
    sc for sc in map(str.strip, os.getenv("FIXED_POSITION_SHOP_CODES", "20655,20656").split(",")) if sc
]
"""各従業員の1日の中のポジション番号を固定とする店舗コードのリスト

通常は各時間帯ごと（15分単位）にスキルの最も高い人から順に番号を割り当てており、結果として人の入れ替わりの多い店舗はポジション番号が細切れになる。
本リストに追加した店舗は、各従業員の1日の中のポジション番号を固定するロジックが適用される。
"""
