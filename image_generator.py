#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片生成模块
功能：将每日信息简报生成美观的图片
"""

from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

class ImageGenerator:
    """图片生成类"""
    
    def __init__(self):
        """初始化图片生成器"""
        # 图片配置
        self.width = 800
        self.height = 1200
        self.bg_color = (255, 255, 255)
        self.text_color = (30, 30, 30)
        self.title_color = (255, 69, 0)
        self.section_color = (0, 100, 200)
        self.border_color = (200, 200, 200)
        self.padding = 40
        self.line_height = 30
        
        # 使用默认字体，确保中文显示正常
        self.title_font = ImageFont.load_default()
        self.section_font = ImageFont.load_default()
        self.content_font = ImageFont.load_default()
    
    def generate_image(self, weather, life_index, almanac, traffic, constellation=None, i_ching=None):
        """
        生成每日信息简报图片
        
        Args:
            weather: 天气信息
            life_index: 生活指数
            almanac: 黄历信息
            traffic: 交通限行信息
            constellation: 星座运势信息
            i_ching: 易经信息
            
        Returns:
            bytes: 图片的字节数据
        """
        # 创建图片
        image = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(image)
        
        # 绘制标题
        today = datetime.now().strftime("%Y年%m月%d日")
        title = f"高端每日信息简报\n{today}"
        title_bbox = draw.textbbox((self.padding, self.padding), title, font=self.title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        draw.text((title_x, self.padding), title, font=self.title_font, fill=self.title_color)
        
        # 绘制分隔线
        y_position = self.padding + 80
        draw.line([(self.padding, y_position), (self.width - self.padding, y_position)], fill=self.border_color, width=2)
        y_position += 30
        
        # 绘制天气早报
        y_position = self._draw_section(draw, "天气早报", y_position)
        weather_items = [
            f"温度：{weather.get('temperature', '未知')}",
            f"天气：{weather.get('weather', '未知')}",
            f"风力：{weather.get('wind', '未知')}",
            f"湿度：{weather.get('humidity', '未知')}"
        ]
        y_position = self._draw_items(draw, weather_items, y_position)
        
        # 绘制生活指南
        y_position = self._draw_section(draw, "生活指南", y_position)
        life_items = [
            f"穿衣：{life_index.get('dressing', '未知')}",
            f"紫外线：{life_index.get('uv', '未知')}",
            f"感冒：{life_index.get('cold', '未知')}",
            f"运动：{life_index.get('sport', '未知')}",
            f"洗车：{life_index.get('car_washing', '未知')}",
            f"空气：{life_index.get('air_quality', '未知')}"
        ]
        y_position = self._draw_items(draw, life_items, y_position)
        
        # 绘制黄历通胜
        y_position = self._draw_section(draw, "黄历通胜", y_position)
        almanac_items = [
            f"农历：{almanac.get('lunar', '未知')}",
            f"生肖：{almanac.get('zodiac', '未知')}",
            f"宜：{almanac.get('suitable', '未知')}",
            f"忌：{almanac.get('avoid', '未知')}"
        ]
        y_position = self._draw_items(draw, almanac_items, y_position)
        
        # 绘制限行提醒
        y_position = self._draw_section(draw, "限行提醒", y_position)
        traffic_items = [
            f"星期：{traffic.get('weekday', '未知')}",
            f"限行：{', '.join(map(str, traffic.get('restricted_numbers', []))) if traffic.get('restricted_numbers') else '不限行'}",
            f"时间：7:00-20:00",
            f"区域：五环路以内"
        ]
        y_position = self._draw_items(draw, traffic_items, y_position)
        
        # 绘制星座运势
        if constellation:
            y_position = self._draw_section(draw, "星座运势", y_position)
            constellation_items = [
                f"今日星座：{constellation.get('constellation', '未知')}",
                f"整体运势：{constellation.get('overall', '未知')}",
                f"爱情运势：{constellation.get('love', '未知')}",
                f"事业运势：{constellation.get('career', '未知')}",
                f"财运运势：{constellation.get('wealth', '未知')}",
                f"健康运势：{constellation.get('health', '未知')}"
            ]
            y_position = self._draw_items(draw, constellation_items, y_position)
        
        # 绘制易经智慧
        if i_ching:
            y_position = self._draw_section(draw, "易经智慧", y_position)
            i_ching_items = [
                f"今日卦象：{i_ching.get('hexagram', '未知')}",
                f"卦象寓意：{i_ching.get('meaning', '未知')}",
                f"幸运数字：{i_ching.get('lucky_number', '未知')}",
                f"幸运颜色：{i_ching.get('lucky_color', '未知')}"
            ]
            y_position = self._draw_items(draw, i_ching_items, y_position)
        
        # 绘制每日寄语
        y_position = self._draw_section(draw, "每日寄语", y_position)
        greeting = "愿您的每一天都充满阳光与希望，事业有成，家庭幸福！"
        draw.text((self.padding + 20, y_position), greeting, font=self.content_font, fill=self.text_color)
        
        # 保存图片到内存
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    def _draw_section(self, draw, title, y_position):
        """
        绘制章节标题
        
        Args:
            draw: ImageDraw对象
            title: 章节标题
            y_position: 当前Y坐标
            
        Returns:
            int: 新的Y坐标
        """
        draw.text((self.padding, y_position), title, font=self.section_font, fill=self.section_color)
        y_position += 30
        return y_position
    
    def _draw_items(self, draw, items, y_position):
        """
        绘制列表项
        
        Args:
            draw: ImageDraw对象
            items: 列表项
            y_position: 当前Y坐标
            
        Returns:
            int: 新的Y坐标
        """
        for item in items:
            draw.text((self.padding + 40, y_position), item, font=self.content_font, fill=self.text_color)
            y_position += self.line_height
        y_position += 20
        return y_position

if __name__ == "__main__":
    """测试图片生成"""
    print("Testing image generation...")
    print("=" * 50)
    
    # 模拟数据 (使用英文，避免编码问题)
    weather = {
        "temperature": "8℃",
        "weather": "Sunny",
        "humidity": "45%",
        "wind": "North 3"
    }
    
    life_index = {
        "dressing": "Comfortable",
        "uv": "Medium",
        "cold": "Low",
        "sport": "Suitable",
        "car_washing": "Suitable",
        "air_quality": "Good"
    }
    
    almanac = {
        "lunar": "Lunar Dec 23",
        "zodiac": "Dragon",
        "suitable": "Sacrifice, Blessing",
        "avoid": "Burial, Kitchen"
    }
    
    traffic = {
        "weekday": "Thursday",
        "restricted_numbers": [4, 9]
    }
    
    constellation = {
        "constellation": "Aries",
        "overall": "⭐⭐⭐⭐",
        "love": "⭐⭐⭐",
        "career": "⭐⭐⭐⭐",
        "wealth": "⭐⭐⭐⭐",
        "health": "⭐⭐⭐"
    }
    
    i_ching = {
        "hexagram": "Xu Gua",
        "meaning": "Strength, Progress, Creation",
        "lucky_number": "4",
        "lucky_color": "Red"
    }
    
    generator = ImageGenerator()
    image_data = generator.generate_image(weather, life_index, almanac, traffic, constellation, i_ching)
    
    # 保存测试图片
    with open("test_briefing.jpg", "wb") as f:
        f.write(image_data)
    
    print("✅ Test image saved as test_briefing.jpg")
    print("Image generation test successful!")
