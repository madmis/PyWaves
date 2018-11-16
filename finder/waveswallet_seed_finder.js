angular.element('#create-seed').scope().vm.generateSeed();
angular.element('#create-seed').scope().vm.seed
angular.element('#create-seed').scope().vm.displayAddress

// https://waveswallet.io/
const vm = angular.element('#create-seed').scope().vm;
let succes = {};
for(let i = 0; true; i++) {
	vm.generateSeed();
	if (wordsList.indexOf(vm.displayAddress) !== -1) {
	    succes[vm.displayAddress] = vm.seed;
		localStorage.setItem(vm.displayAddress, vm.seed);
	}

    if (i % 10000 === 0) {
        console.log(i);
        console.log(succes);
    }
}