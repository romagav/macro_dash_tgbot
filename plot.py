import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO

plt.rcParams['font.family'] = 'DejaVu Sans'


def create_dollar_chart(df, title="Курс USD/RUB"):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['date'], df['rate'], color='steelblue', linewidth=2, label='Курс USD')
    df['MA14'] = df['rate'].rolling(window=14).mean()
    ax.plot(df['date'], df['MA14'], color='red', linestyle='--', linewidth=1.5, label='Скользящая средняя (14 дней)')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel('Рублей за доллар')
    ax.set_xlabel('Дата')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    return buf


def create_key_rate_chart(df, title="Ключевая ставка ЦБ РФ"):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.step(df['date'], df['rate'], where='post', color='darkred', linewidth=2.5, label='Ключевая ставка')
    ax.fill_between(df['date'], 0, df['rate'], step='post', alpha=0.1, color='darkred')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel('Проценты годовых')
    ax.set_xlabel('Дата')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    return buf
