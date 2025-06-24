#!/bin/bash
main ()
{
	while true; do
clear
echo "1 - Cadastro de usuário"
echo "2 - Cadastro de grupo de trabalho"
echo "3 - Sair"
read num 
case $num in 
"1")
cadastro_usuario ;;
"2")
cadastro_grupo ;;
"3")
break ;;
esac
done
}
cadastro_usuario ()
{
echo "Entre com seu usuário e senha"
read nome
echo "Entre com a senha"
read senha
seradd -m $nome -p $senha
chage -d 0 $nome
}
cadastro_grupo ()
{
echo "Entre com o grupo de trabalho"
read grupo
groupadd $grupo
}
sair ()
{
break
}
main
