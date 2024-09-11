import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    # 1. Creare un nuovo utente
    print("Creazione di un nuovo utente...")
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "role": "customer"
    }
    response = requests.post(f"{BASE_URL}/users/users/", json=user_data)
    print(f"Risposta: {response.status_code}")
    print(response.json())
    
    # 2. Autenticazione e ottenimento del token
    print("\nAutenticazione...")
    auth_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/users/token", data=auth_data)
    print(f"Risposta: {response.status_code}")
    token_data = response.json()
    print(token_data)

    
    if "access_token" not in token_data:
        print("Autenticazione fallita. Impossibile procedere con i test.")
        return
    
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }
    
    # 3. Ottenere le informazioni dell'utente corrente
    print("\nOttenimento delle informazioni dell'utente...")
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Risposta: {response.status_code}")
    print(response.json())
    
    # 4. Aggiornare le informazioni dell'utente
    print("\nAggiornamento delle informazioni dell'utente...")
    update_data = {
        "email": "updated@example.com"
    }
    user_id = response.json()["id"]
    response = requests.put(f"{BASE_URL}/users/{user_id}", headers=headers, json=update_data)
    print(f"Risposta: {response.status_code}")
    print(response.json())
    
    # 5. Eliminare l'utente
    print("\nEliminazione dell'utente...")
    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    print(f"Risposta: {response.status_code}")
    
    # 6. Verificare che l'utente sia stato eliminato
    print("\nVerifica dell'eliminazione dell'utente...")
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Risposta: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    test_api()

