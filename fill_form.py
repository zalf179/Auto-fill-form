import pandas as pd
import random
import time

from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfmEwN5Gyaipdzy2Mw57o6IEjNf12bpKm8EDi1aBjyhJUWc3A/viewform"

LIKERT_CHOICES = [
    "Netral",
    "Setuju",
    "Sangat Setuju"
]

LIKERT_WEIGHTS = [
    20,  # Netral
    50,  # Setuju
    30   # Sangat Setuju
]


def fill_one_response(page, row):
    page.goto(FORM_URL, wait_until="networkidle")

    text_inputs = page.locator('input[type="text"]')

    text_inputs.nth(0).fill(str(row["nama"]))
    text_inputs.nth(1).fill(str(row["email"]))
    text_inputs.nth(2).fill(str(row["umur"]))
    text_inputs.nth(3).fill(str(row["jabatan"]))
    text_inputs.nth(4).fill(str(row["masa_kerja"]))

    gender = str(row["gender"]).strip().upper()

    if "PEREMPUAN" in gender:
        page.get_by_text("PEREMPUAN", exact=True).click()
    else:
        page.get_by_text("LAKI - LAKI", exact=True).click()

    page.wait_for_timeout(1000)

    radio_groups = page.locator('[role="radiogroup"]')
    total_groups = radio_groups.count()

    print(f"  Total radiogroup ditemukan: {total_groups}")

    # Index 0 adalah gender, Likert mulai dari index 1
    likert_start = 1

    for i in range(likert_start, total_groups):
        answer = random.choices(
            LIKERT_CHOICES,
            weights=LIKERT_WEIGHTS,
            k=1
        )[0]

        group = radio_groups.nth(i)
        group.wait_for(state="visible")

        clicked = False

        # Strategy 1: span dengan teks persis
        option = group.locator(f'span[dir="auto"]:text-is("{answer}")')
        if option.count() > 0:
            option.first.click()
            clicked = True

        # Strategy 2: data-value attribute
        if not clicked:
            option = group.locator(f'[data-value="{answer}"]')
            if option.count() > 0:
                option.first.click()
                clicked = True

        # Strategy 3: get_by_text fallback
        if not clicked:
            try:
                group.get_by_text(answer, exact=True).first.click()
                clicked = True
            except Exception as e:
                print(f"  [ERROR] Grup {i} gagal diklik: {e}")

        print(f"  Pertanyaan {i}: '{answer}' — {'✓' if clicked else '✗ GAGAL'}")

        page.wait_for_timeout(300)

    # Klik tombol Submit
    submit_button = page.get_by_role("button")

    for i in range(submit_button.count()):
        btn = submit_button.nth(i)

        try:
            text = btn.inner_text().strip().lower()

            if text in ["kirim", "submit"]:
                btn.click()
                print("  Form berhasil disubmit ✓")
                break
        except:
            pass

    page.wait_for_timeout(2000)


def main():
    df = pd.read_excel("data.xlsx", engine="openpyxl")

    print(f"Total data: {len(df)} baris\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for idx, row in df.iterrows():
            print(f"[{idx + 1}/{len(df)}] Mengisi: {row['nama']}")

            try:
                fill_one_response(page, row)
            except Exception as e:
                print(f"  [ERROR] Baris {idx + 1} gagal: {e}")

            delay = random.uniform(2, 5)
            print(f"  Menunggu {delay:.1f} detik...\n")
            time.sleep(delay)

        browser.close()
        print("Selesai!")


if __name__ == "__main__":
    main()