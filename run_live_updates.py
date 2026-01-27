import os
import time
import subprocess
import django
from django.utils import timezone
from datetime import datetime, timedelta

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from matches.models import Match

# Configuração de Intervalos
LIVE_UPDATE_INTERVAL = 15  # Segundos entre checagens de jogos ao vivo
FULL_SYNC_INTERVAL = 3600  # Segundos (1 hora) entre sincronizações completas (Resultados + Próximos)

last_full_sync = None

def run_live_update():
    """
    Atualiza apenas jogos que estão acontecendo AGORA ou começando em breve.
    É leve e rápido.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔴 Buscando jogos ao vivo...")
    try:
        # Verifica se há necessidade de rodar (jogos ao vivo ou próximos 30min)
        now = timezone.now()
        buffer_time = now + timedelta(minutes=30)
        
        # Otimização: Só chama o script pesado se tiver jogo no banco marcado como Live ou Scheduled para agora
        # Mas atenção: se o banco estiver desatualizado, ele pode não saber que tem jogo.
        # Por isso o Full Sync é importante.
        live_or_soon = Match.objects.filter(
            date__lte=buffer_time,
            status__in=['Scheduled', 'Live', '1H', 'HT', '2H', 'ET', 'PEN', 'IN_PLAY']
        ).exclude(status__in=['Finished', 'Postponed', 'Cancelled'])

        if live_or_soon.exists():
            subprocess.run(["python", "manage.py", "update_live_matches", "--mode", "live"], check=True)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 💤 Nenhum jogo ao vivo no momento.")
            
    except Exception as e:
        print(f"❌ Erro na atualização ao vivo: {e}")

def run_full_sync():
    """
    Atualiza TUDO: Resultados de hoje, jogos de ontem (se tiver), e calendário dos próximos 14 dias.
    Garante que jogos finalizados vão para a tabela de Resultados.
    """
    global last_full_sync
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 Iniciando Sincronização Completa (Resultados + Calendário)...")
    try:
        # mode='upcoming' na verdade busca de HOJE até +14 dias, então pega resultados do dia também
        subprocess.run(["python", "manage.py", "update_live_matches", "--mode", "upcoming"], check=True)
        last_full_sync = datetime.now()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Sincronização Completa finalizada.")
    except Exception as e:
        print(f"❌ Erro na sincronização completa: {e}")

if __name__ == "__main__":
    print("="*50)
    print("🚀 StatsFut Auto-Updater Iniciado")
    print("="*50)
    print(f"Intervalo Live: {LIVE_UPDATE_INTERVAL}s")
    print(f"Intervalo Full Sync: {FULL_SYNC_INTERVAL}s")
    print("="*50)

    # Força um sync completo ao iniciar para garantir dados frescos
    run_full_sync()

    while True:
        try:
            # Verifica se está na hora do Full Sync
            if not last_full_sync or (datetime.now() - last_full_sync).total_seconds() > FULL_SYNC_INTERVAL:
                run_full_sync()
            
            # Roda atualização Live
            run_live_update()
            
            # Aguarda próximo ciclo
            time.sleep(LIVE_UPDATE_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoramento paralisado pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro fatal no loop principal: {e}")
            time.sleep(60)
