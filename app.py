import streamlit as st
from PIL import Image, ExifTags
from geopy.geocoders import Nominatim

# Função para extrair e exibir todos os metadados EXIF da imagem
def display_exif_data(image):
    try:
        # Extrai os metadados EXIF
        exif_data = image._getexif()
        if exif_data is not None:
            # Exibir todos os metadados EXIF
            st.write("Metadados EXIF da Imagem:")
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)  # Obter nome legível para o tag
                st.write(f"{tag_name}: {value}")
            return exif_data
        else:
            st.write("Nenhum metadado EXIF encontrado.")
            return None
    except Exception as e:
        st.error(f"Erro ao obter os metadados EXIF: {e}")
        return None

# Função para converter coordenadas GPS de DMS para formato decimal
def convert_to_decimal(degrees, minutes, seconds):
    try:
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    except Exception as e:
        st.error(f"Erro ao converter coordenadas GPS: {e}")
        return None

# Função para extrair os metadados GPS
def get_location_from_exif(exif_data):
    try:
        if exif_data:
            gps_info = None
            for tag, value in exif_data.items():
                if ExifTags.TAGS.get(tag) == 'GPSInfo':
                    gps_info = value
                    break

            if gps_info is not None:
                # Extraímos a latitude e longitude
                lat_deg = gps_info[2][0]
                lat_min = gps_info[2][1]
                lat_sec = gps_info[2][2]
                lon_deg = gps_info[4][0]
                lon_min = gps_info[4][1]
                lon_sec = gps_info[4][2]

                # Convertendo as coordenadas para o formato decimal
                lat = convert_to_decimal(lat_deg, lat_min, lat_sec)
                lon = convert_to_decimal(lon_deg, lon_min, lon_sec)

                # Retorna as coordenadas GPS
                return lat, lon
        return None, None
    except Exception as e:
        st.error(f"Erro ao extrair localização: {e}")
        return None, None

# Interface Streamlit
st.title('Teste de Extração de Localização e Metadados EXIF')

uploaded_file = st.file_uploader("📷 Carregue uma imagem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem carregada", use_column_width=True)

    # Exibir os metadados EXIF
    exif_data = display_exif_data(image)

    # Tentar obter a localização GPS a partir dos metadados EXIF
    lat, lon = get_location_from_exif(exif_data)
    if lat and lon:
        st.markdown(f"### 🌍 Localização GPS: Latitude {lat}, Longitude {lon}")
    else:
        st.markdown("### 🌍 Não foi possível obter a localização GPS.")
