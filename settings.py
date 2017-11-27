"""設定ファイル."""
import os

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')  # ログファイルディレクトリ

# ログファイルディレクトリがなければ作成する
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING_CONF = {
    'version': 1,  # 必須
    # logger設定処理が重複しても上書きする
    'disable_existing_loggers': True,
    # 出力フォーマットの設定
    'formatters': {
        'default': {  # デフォルトのフォーマット
            '()': 'colorlog.ColoredFormatter',  # colorlogライブラリを適用
            'format': '\t'.join([
                "%(log_color)s[%(levelname)s]",  # ログレベル
                "asctime:%(asctime)s",  # ログの出力日時
                "process:%(process)d",  # ログ出力が実行されたプロセス名
                "thread:%(thread)d",  # ログ出力が実行されたスレッドID
                "module:%(module)s",  # ログ出力が実行されたモジュール名
                "%(pathname)s:%(lineno)d",  # ログ出力が実行されたモジュールのパスと行番号
                "message:%(message)s",  # ログ出力されるメッセージ
            ]),
            'datefmt': '%Y-%m-%d %H:%M:%S',  # asctimeで出力されるログ出力日時の形式
            # ログレベルに応じて色をつける
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'simple': {  # ログ出力要素を減らしたシンプル版のフォーマット
            '()': 'colorlog.ColoredFormatter',  # pip install colorlog
            'format': '\t'.join([
                "%(log_color)s[%(levelname)s]",
                "%(asctime)s",
                "%(message)s",  # 書式はログレベル、ログ出力日時、メッセージのみ
            ]),
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'query': {  # SQLクエリのログ出力用フォーマット
            '()': 'colorlog.ColoredFormatter',
            'format': '%(cyan)s[SQL] %(message)s',  # クエリのみ出力する
        },
    },
    # ログの出力先を決めるハンドラーの設定
    'handlers': {
        'file': {  # ファイルにログを出力するハンドラー設定
            'level': 'DEBUG',  # logger.levelがDEBUG 以上で出力
            # ログサイズが一定量を超えると自動的に新しいログファイルを作成 (ローテート) するハンドラー
            'class': 'logging.handlers.RotatingFileHandler',
            # ログファイルのパスを指定
            'filename': os.path.join(LOG_DIR, 'crawler.log'),
            'formatter': 'default',  # このハンドラではデフォルトのフォーマットでログを出力する
            'backupCount': 3,  # 古くなったログファイルは3世代分保持する指定
            'maxBytes': 1024 * 1024 * 2,  # ログサイズが2MBを超えたらログファイルをローテート
        },
        'console': {  # ターミナルにログを出力するハンドラー設定
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # ターミナルにログを出力するハンドラー
            'formatter': 'default',  # このハンドラではデフォルトのフォーマットでログを出力する
        },
        'console_simple': {  # ターミナルにログを出力するハンドラーのシンプルフォーマット版
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',  # シンプル版のフォーマットを指定
        },
        'query': {  # ターミナルにSQLクエリログを出力するハンドラー
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'query',  # SQLクエリ用フォーマットを指定
        },
    },
    'root': {  # デフォルト設定
        'handlers': ['file', 'console_simple'],  # 先述のfile, consoleの設定で出力
        'level': 'DEBUG',
    },
    # ロガー名と、ロガーに紐づくハンドラ、ログレベルの設定
    'loggers': {
        # logging.getLogger(__name__) の __name__ で参照される名前がキーになる
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',  # CeleryのログはWARNING以上しか出さない
            'propagate': False,  # rootロガーにログイベントを渡さない指定
        },
        'my_project': {  # my_project.pyモジュールで使うためのロガー
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
