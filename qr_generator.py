import qrcode

def generate_qr(link, save_path):
    img = qrcode.make(link)
    img.save(save_path)
