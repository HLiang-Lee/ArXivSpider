from bs4 import BeautifulSoup  
import requests  
import openpyxl
# 假设这是你要抓取的页面的URL  
url = "https://arxiv.org/category_taxonomy"  
  
# 发送HTTP请求获取页面内容  
response = requests.get(url)  
response.raise_for_status()  # 如果请求失败，这将抛出异常  
  
# 使用BeautifulSoup解析页面内容  
soup = BeautifulSoup(response.text, 'html.parser')  
  
# 查找所有具有指定类的<h2>标签  
h2_tags = soup.find_all('h2', class_='accordion-head')  
  
tables = []
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["Category", "SubCat_code", "SubCat_name", "SubCat_Desc"])
# 遍历每个<h2>标签  
for h2 in h2_tags:  
    # 查找紧随<h2>标签的<div class="accordion-body">  
    category = h2.get_text(strip=True)
    accordion_body = h2.find_next_sibling('div', class_='accordion-body')  
    if accordion_body:  
        # 在<div class="accordion-body">中查找所有的<h4>标签  
        h4_tags = accordion_body.find_all('div', class_='column is-one-fifth')  
        for h4 in h4_tags:  
            # 提取<h4>标签中的文本，包括cs.AI和(Artificial Intelligence)  
            subject_code = h4.find('span').text.strip() if h4.find('span') else ""  
            subject_name = h4.text.strip().replace(subject_code, "").strip()  
              
            # 查找与<h4>标签同级且紧随其后的<div class="column"><p>标签  
            p_tag = h4.find_next_sibling('div', class_='column').find('p')
            print(p_tag)  
            if p_tag:  
                # 提取<p>标签中的文本内容  
                paragraph_text = p_tag.get_text(strip=True)  
                
                ws.append([category, subject_code, subject_name, paragraph_text])
                # 打印或处理提取的信息  
                print(f"Subject Code: {subject_code}, Subject Name: {subject_name}, Description: {paragraph_text}")
wb.save("/path/to/ArXivSpider/ArXivCategory.xlsx")