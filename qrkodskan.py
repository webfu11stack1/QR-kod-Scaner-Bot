import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import cv2
from io import BytesIO
import qrcode
from aiogram.dispatcher import FSMContext
from pyzbar.pyzbar import decode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
logging.basicConfig(level=logging.INFO)
bot_token = ""
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)




@dp.message_handler(commands=['start'])
async def on_start(message: types.Message,state:FSMContext):
    video="https://i0.wp.com/pediaa.com/wp-content/uploads/2022/05/QR-Code.png?fit=640%2C563&ssl=1"
    await message.answer_photo(photo=video,caption="""‼️Salom! Men QR kodlarni <b>Skanerlovchi</b> va <b>Yaratuvchi</b> botman. 
\n<b>⚙️Qr kod yasash uchun matn yuboring✅</b> \n<b>🔎Qr kod scanerlash uchun rasm yuboring✅</b>""",parse_mode="HTML")
    await state.set_state("Qr")


@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.PHOTO],state="Qr")
async def handle_text_or_photo(message: types.Message):
    try:
        if message.content_type == types.ContentType.TEXT:
            # Matn yuborilgan
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(message.text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_byte_array = BytesIO()
            img.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)
            await message.reply_photo(
                types.InputFile(img_byte_array, filename="qr.png"),
                caption=f"{message.text}\n\nQR kod @qr_code_scanner_create_bot orqali yaratildi✅"
            )
        elif message.content_type == types.ContentType.PHOTO:
            # Rasm yuborilgan
            photo = message.photo[-1]
            file_id = photo.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, 'image.jpg')
            image = cv2.imread('image.jpg')
            decoded_objects = decode(image)
            
            if decoded_objects:
                qr_code_data = decoded_objects[0].data.decode('utf-8')
                await message.reply(f'❗️QR kod natijasi:\n\n✅ : {qr_code_data}')
            else:
                await message.reply('❌QR kod topilmadi. Rasmni to\'g\'ri kiriting.')
    except Exception as e:
        await message.reply(f'Xato: {str(e)}')


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
