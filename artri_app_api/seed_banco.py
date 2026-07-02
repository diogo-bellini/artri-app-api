import csv
import os
import django

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artri_app_api.settings')
django.setup()

from authentication.models import Exercise, Training, TrainingExercise

# Mapeamento para todas as possíveis variações que você pode digitar na planilha
diff_map = {
    'FÁCIL': 'Easy', 'FACIL': 'Easy', 'INICIANTE': 'Easy',
    'MÉDIO': 'Medium', 'MEDIO': 'Medium', 'INTERMEDIÁRIO': 'Medium', 'INTERMEDIARIO': 'Medium',
    'DIFÍCIL': 'Hard', 'DIFICIL': 'Hard', 'AVANÇADO': 'Hard', 'AVANCADO': 'Hard'
}

def reset_and_seed(csv_path):
    print("⚠️  ATENÇÃO: Apagando todos os Treinos e Exercícios antigos do banco...")
    Training.objects.all().delete()
    Exercise.objects.all().delete()
    # O TrainingExercise é apagado automaticamente pelo Django (efeito Cascata)
    print("✅ Banco limpo com sucesso!\n")

    print(f"📖 Lendo o arquivo {csv_path} e recriando os dados...")
    
    # Dicionário para controlar a ordem dos exercícios dentro de cada treino
    training_order = {}
    exercicios_processados = 0
    
    with open(csv_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';')
        # Limpa os cabeçalhos para evitar erros com espaços invisíveis
        reader.fieldnames = [str(field).strip() for field in reader.fieldnames if field]
        
        for row in reader:
            clean_row = {str(k).strip(): str(v).strip() for k, v in row.items() if k is not None}
            
            ex_name = clean_row.get('Nome do exercício')
            if not ex_name:
                continue # Pula linhas vazias
                
            sets = clean_row.get('Séries e Repetições', '')
            rest = clean_row.get('Descanso', '')
            obs = clean_row.get('Instruções/Observações', '')
            link = clean_row.get('Link do vídeo', '')
            diff_pt = clean_row.get('Dificuldade', 'Fácil').upper()
            treino_name = clean_row.get('Treino', 'Treino Geral')
            
            # Limpa links incorretos copiados do Excel
            if 'Mesmo' in link or 'Mesmo' in obs:
                link = ''
                
            db_diff = diff_map.get(diff_pt, 'Easy')
            
            # 1. Cria o Exercício (usamos get_or_create para não duplicar no banco
            # caso o mesmo exercício exato seja usado em treinos diferentes)
            exercise, _ = Exercise.objects.get_or_create(
                name=ex_name,
                difficulty=db_diff,
                defaults={
                    'sets_reps': sets,
                    'rest_time': rest,
                    'description': obs,
                    'tutorial_link': link
                }
            )
            exercicios_processados += 1
            
            # 2. Cria ou pega o Treino
            training, _ = Training.objects.get_or_create(
                name=treino_name,
                defaults={
                    'difficulty': db_diff,
                    'description': f'Exercícios focados em: {treino_name.title()}'
                }
            )
            
            # 3. Inicializa o contador de ordem para este treino (se for a primeira vez)
            if treino_name not in training_order:
                training_order[treino_name] = 0
                
            # 4. Vincula o Exercício ao Treino mantendo a ordem exata da planilha (0, 1, 2...)
            TrainingExercise.objects.create(
                training=training,
                exercise=exercise,
                order=training_order[treino_name]
            )
            
            training_order[treino_name] += 1

    print("\n🎉 Sucesso! Processo concluído.")
    print(f"🏋️  Total de exercícios mapeados: {exercicios_processados}")
    print(f"📋 Treinos criados ({len(training_order)}):")
    for t_name, count in training_order.items():
        print(f"   - {t_name}: {count} exercícios vinculados ordenadamente.")

if __name__ == '__main__':
    # Coloque o nome exato do seu arquivo CSV atual
    reset_and_seed('Exercícios ArtriApp - Exercícios ArtriApp - Exercícios.csv')