#include <iostream>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <SFML/Graphics.hpp>
#include "RichText.hpp"

using namespace std;

long** initmatr(string filename, int& n, int& m)
// Инициализация динамической матрицы из файла
{
	ifstream ft(filename);
	// Проверка на возможность открыть файл
	if (!ft.is_open())
	{
		cout << "The file can't be opened" << endl;
		exit(0);
	}
	// Создание указателя на динамическую матрицу (как массива массивов)
	long** matr;
	ft >> n >> m;
	// Выделение памяти для матрицы
	matr = new long* [n];
	for (int i = 0; i < n; i++)
	{
		// Выделение памяти для каждого из массивов
		matr[i] = new long[m];
		for (int j = 0; j < m; j++)
			ft >> matr[i][j];			
	}
	ft.close();

	return matr;
}

long getMiddle(long* mass, int n)
// Возвращает среднее значение массива из n элементов
{
	long sum = 0;
	for (int i = 0; i < n; i++)
		sum += mass[i];
	return (sum / n);
}

long getCloseElement(long* mass, int n)
// Возвращает элемент массива, наиболее близкий к среднему значению
{
	long middle = getMiddle(mass, n), differ = abs(mass[0] - middle);
	int num = 0;
	for (int i = 1; i < n; i++)
	{
		long newdiffer = abs(mass[i] - middle);
		if  (newdiffer < differ)
		{
			differ = newdiffer;
			num = i;
		}
	}
	return mass[num];
}

sfe::RichText printmatr(long** matr, int n, int m, sf::Vector2f position, sf::Font &font, 
						sf::Color special=sf::Color(186, 16, 5), string previous_text = "Your matrix",
						sf::Color maincolor=sf::Color(0,0,0), int size=25)
/* Создание текста для вывода на экран динамической матрицы
   position устанавливает позицию текста в графическом поле
   font -- шрифт написания текста
   special -- цвет выделяющегося текста (по умолчанию RGB(186, 16, 5))
   maincolor -- цвет основного текста (по умолчанию чёрный)
   size -- размер симоволов в пикселях (по умолчанию 25)
   previous_text -- подпись перед матрицей (по умолчанию Your matrix)*/
{
	sfe::RichText matrixText(font);
	ostringstream matrix_str;
	// Используя потоки, выводим матрицу в строку, чтобы затем 
	// поместить её в переменную типа Text для вывода на экран
	matrixText << maincolor << previous_text << "\n";
	for (int i = 0; i < n; i++)
	{
		long close_elem = getCloseElement(matr[i], m);
		for (int j = 0; j < m; j++)
		{
			matrix_str.str("");
			matrix_str << setw(12) << matr[i][j];
			if (matr[i][j] == close_elem)
				matrixText << sf::Text::Bold << special << matrix_str.str();
			else
				matrixText << sf::Text::Regular << maincolor << matrix_str.str();
		}
		matrixText << "\n";
	}

	matrixText.setCharacterSize(size);
	matrixText.setPosition(position);
	return matrixText;
}

int main()
{
	// Создание окна
	sf::RenderWindow window(sf::VideoMode(1000, 600, 32), "Hryshalevich kr",
							sf::Style::Close | sf::Style::Titlebar);

	long** matr;
	int n, m;
	matr = initmatr("matrix.txt", n, m);

	sfe::RichText matr_text;
	sf::Text signature_text;
	sf::Font font, signature_font, new_font;
	if (!font.loadFromFile("fonts/GOTHIC.ttf"))
	{
		cout << "Error" << endl;
		exit(0);
	}
	if (!signature_font.loadFromFile("fonts/FTLTLT.ttf"))
	{
		cout << "Error" << endl;
		exit(0);
	}

	matr_text = printmatr(matr, n, m, sf::Vector2f(50.0, 100.0), font);
	
	// Область для подписи внизу экрана
	sf::RectangleShape signature(sf::Vector2f(250.0, 100.0));
	signature.setFillColor(sf::Color(226, 211, 128));
	signature.setPosition(sf::Vector2f(780.0, 530.0));
	// Текст подписи
	signature_text.setString("Hryshalevich");
	signature_text.setFont(signature_font);
	signature_text.setFillColor(sf::Color::Black);
	signature_text.setCharacterSize(30);
	signature_text.setPosition(sf::Vector2f(800.0, 550.0));

	while (window.isOpen())
	{
		sf::Event event;

		if (window.pollEvent(event))
		{
			switch (event.type)
			{
			case sf::Event::Closed:
				window.close();
				break;
			}
		}
		window.clear(sf::Color(120, 172, 215));
		window.draw(matr_text);
		window.draw(signature);
		window.draw(signature_text);
		window.display();
	}

	// Освобождение памяти от матрицы
	for (int i = 0; i < n; i++)
	{
		delete[] matr[i];
	}
	delete[] matr;
	return 0;
}