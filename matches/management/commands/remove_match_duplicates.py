from django.core.management.base import BaseCommand
from django.db.models import Count
from matches.models import Match

class Command(BaseCommand):
    help = "Remove jogos duplicados (mesma temporada, mandante e visitante)"

    def handle(self, *args, **options):
        # Nova lógica: Agrupa por Temporada + Mandante + Visitante
        # Isso garante que times joguem apenas UMA vez com mando de campo por temporada
        duplicates = (
            Match.objects.values('season', 'home_team', 'away_team')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        total_groups = duplicates.count()
        total_deleted = 0
        
        self.stdout.write(f"Encontrados {total_groups} confrontos duplicados (mesma temporada/mandante/visitante).")

        for item in duplicates:
            matches = Match.objects.filter(
                season=item['season'],
                home_team=item['home_team'],
                away_team=item['away_team']
            )
            
            # Critério de desempate para manter o "melhor" jogo:
            # 1. Tem API ID (veio da API paga/oficial)
            # 2. Tem status 'Finished'
            # 3. Tem placar (home_score não é nulo)
            # 4. Data mais recente (assumindo correção)
            # 5. ID maior (último inserido)
            
            sorted_matches = sorted(matches, key=lambda m: (
                1 if m.api_id else 0,
                1 if m.status == 'Finished' else 0,
                1 if m.home_score is not None else 0,
                m.date,
                m.id
            ), reverse=True)
            
            keep = sorted_matches[0]
            delete_list = sorted_matches[1:]
            
            for m in delete_list:
                self.stdout.write(f"Removendo duplicata: {m.home_team} vs {m.away_team} ({m.date}) [ID: {m.id}]")
                m.delete()
                total_deleted += 1
                
        self.stdout.write(self.style.SUCCESS(f"Limpeza concluída. Removidos {total_deleted} jogos duplicados."))
