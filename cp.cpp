#include <iostream>
#include <string> // Necessário para usar std::string

int main() {
	// Declaração de variáveis
	std::string nome;
	int anoNascimento;
	int anoAtual = 2025; // Estamos em 2025

	// Pede o nome do usuário
	std::cout << "Olá! Por favor, digite seu nome: ";
	std::getline(std::cin, nome); // Usa getline para ler nomes com espaço

	// Pede o ano de nascimento do usuário
	std::cout << "Agora, digite o ano em que você nasceu: ";
	std::cin >> anoNascimento;

	// Calcula a idade
	int idade = anoAtual - anoNascimento;

	// Imprime a saudação final
	std::cout << "\n--- Resultado ---\n"; // \n cria uma nova linha
	std::cout << "Prazer em te conhecer, " << nome << "!\n";
	std::cout << "Pelas minhas contas, você tem ou fará " << idade << " anos em " << anoAtual << ".\n";

	return 0;
}