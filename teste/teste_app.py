from app import main


def test_main_imprime_hello_world(capsys):
    main()

    saida = capsys.readouterr()
    assert saida.out == "Hello, World!\n"
