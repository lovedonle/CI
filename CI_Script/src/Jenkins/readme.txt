1. 打包完后的状态字典会比依赖字典多一项"payment-parent"
2. 执行完成后只需比较：依赖字典=状态字典-1
3. dict 依赖文件格式：
				payment-ac-entity []
				payment-ac-dao ['payment-ac-entity']
				payment-ac-api ['payment-ac-entity','payment-ac-dao','payment-common']
				或者
				payment-ac-entity': []
				payment-ac-dao': [payment-ac-entity]
				payment-ac-api': [payment-ac-entity,payment-ac-dao,payment-common]
				或者：
				'payment-ac-entity': []
				'payment-ac-dao': ['payment-ac-entity']
				'payment-ac-api': ['payment-ac-entity','payment-ac-dao','payment-common']

	key,value的引号可选;但是他们之间必须要用冒号或者空格隔开,value值必须用 []包含起来,value的各子项用逗号分开,逗号前后可以包含空格；一行一个依赖项目，一行前后可以包含空格。

	
	eclipse快捷键：
	按住Ctrl+Alt+Down，即可以在下面快速复制一行，按住Ctrl+Alt+Up，即可以在上面快速复制一行
	