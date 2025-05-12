import streamlit as st
from PIL import Image, ExifTags
from geopy.geocoders import Nominatim

# Função para extrair os metadados EXIF e buscar a localização
def get_location_from_exif(image):
    try:
        # Extrai os metadados EXIF
        exif_data = image._getexif()
        if exif_data is not None:
            # Localiza o índice para a GPSInfo
            gps_info = None
            for tag, value in exif_data.items():
                if ExifTags.TAGS.get(tag) == 'GPSInfo':
                    gps_info = value
                    break
            
            if gps_info is not None:
                # Extraímos a latitude e longitude
                lat_deg = gps_info[2][0] / gps_info[2][1]
                lon_deg = gps_info[4][0] / gps_info[4][1]
                
                # Usamos o geopy para converter as coordenadas em um endereço
                geolocator = Nominatim(user_agent="geoapiExercises")
                location = geolocator.reverse((lat_deg, lon_deg), language='en')
                return location.address
        return None
    except Exception as e:
        st.error(f"Erro ao obter a localização EXIF: {e}")
        return None

# Interface Streamlit
st.title('Teste de Extração de Localização de Imagem')

uploaded_file = st.file_uploader("📷 Carregue uma imagem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem carregada", use_column_width=True)

    # Tentar obter a localização
    location = get_location_from_exif(image)
    if location:
        st.markdown(f"### 🌍 Localização da Imagem: {location}")
    else:
        st.markdown("### 🌍 Não foi possível obter a localização.")
