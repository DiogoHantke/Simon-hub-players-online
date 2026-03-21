import requests
import time

ESP_SCORE = 1 

while True:
    try:
        response = requests.post(
            "http://localhost:5000/score",
            json={"score_player": ESP_SCORE}
        )
        data = response.json()  

        status = data.get('status')
        print(f"Servidor respondeu: {status}")

        if status == 'pause':
            print("Jogador pendente, aguardando nome...")
            time.sleep(3)
            continue
        elif status == 'ok':
            print(f"Pontuação {ESP_SCORE} enviada com sucesso!")
            ESP_SCORE += 1  
        else:
            print("Resposta inesperada do servidor:", data)

    except requests.exceptions.ConnectionError:
        print('Servidor não encontrado, tentando novamente em 3s...')
        time.sleep(3)
    except Exception as e:
        print('Erro inesperado:', e)

    time.sleep(5)  