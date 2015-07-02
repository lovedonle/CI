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
4.eclipse快捷键：
	按住Ctrl+Alt+Down, 即可以在下面快速复制一行，按住Ctrl+Alt+Up, 即可以在上面快速复制一行
	按住shit+up/down, 即可移动当前行
5.package.py：
	1)分析整个指定目录下的工程间的依赖关系，生成dict.txt文件，该步骤中如果遇到问题不会停止，会最终生成dict.txt，
	但是可能有部分工程会因为代码原因分析失败，依赖关系不会存入该文件，会在下一步中体现出来，下一步中会立刻停止
	2)根据生成的dict.txt文件，对所有工程进行打包，或者也可以指定某一个子工程进行打包，详细参数请参考脚本文件注释。该步骤中如果遇到错误会立刻停止
6.deploy.py：将指定文件夹下的jar和war包拷贝到相应的部署目录下，并重启服务（配置修改待完善）
7.Copy.sh:拷贝指定目录下的jar、war文件
8.Jenkins.ini:所有的外部输入变量放到配置文件