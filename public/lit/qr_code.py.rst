QR-Code
=======

::

  import streamlit as st
  import qrcode
  from PIL import Image

  st.set_page_config(page_title="QR Code Generator", page_icon="🔳")

  st.title("🔳 QR Code Generator")

  data = st.text_input("Text / URL to encode", value="https://example.com")

  col1, col2 = st.columns(2)
  with col1:
      box_size = st.slider("Box size", min_value=2, max_value=20, value=10)
  with col2:
      border = st.slider("Border", min_value=1, max_value=10, value=4)

  error_correction_label = st.selectbox(
      "Error correction",
      ["L (7%)", "M (15%)", "Q (25%)", "H (30%)"],
      index=1,
  )
  ec_map = {
      "L (7%)": qrcode.constants.ERROR_CORRECT_L,
      "M (15%)": qrcode.constants.ERROR_CORRECT_M,
      "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
      "H (30%)": qrcode.constants.ERROR_CORRECT_H,
  }

  if not data.strip():
      st.warning("Please enter some text.")
  else:
      qr = qrcode.QRCode(
          version=None,  # auto
          error_correction=ec_map[error_correction_label],
          box_size=box_size,
          border=border,
      )
      qr.add_data(data)
      qr.make(fit=True)

      img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

      st.subheader("Preview")
      st.image(img, caption="Generated QR code", use_container_width=False)

      # Offer download
      import io
      buf = io.BytesIO()
      img.save(buf, format="PNG")
      st.download_button(
          "Download PNG",
          data=buf.getvalue(),
          file_name="qrcode.png",
          mime="image/png",
      )

  st.caption("Tip: install dependencies with `pip install streamlit qrcode[pil] pillow`")
