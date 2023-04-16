import requests
file_url = "https://doc-10-c4-docs.googleusercontent.com/docs/securesc/jc5i569vdkqodk6r2o520id7h420e1vo/s364psv5rar9jvrc8mnh4rj5ja4gciu7/1681578525000/14307910142276457959/00188764112960779471Z/1kONyJWpS4jErkRzboeWVCwKUzzsarx2X?e=download&uuid=75ef46ab-0aff-4f70-9c39-b75734386993&nonce=vgq5fla6354vs&user=00188764112960779471Z&hash=24egig9quai87p9kjbqbtk6h0pklh1dh"
  
r = requests.get(file_url, stream = True)
  
with open("python.pdf","wb") as pdf:
    for chunk in r.iter_content(chunk_size=1024*1024):
  
         # writing one chunk at a time to pdf file
         if chunk:
             pdf.write(chunk)