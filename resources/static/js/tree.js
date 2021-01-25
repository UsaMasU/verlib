'use strict';

const STORAGE_NAME = 'program_library';

let details = document.querySelectorAll('.treeHTML details');
let summary = document.querySelectorAll('.treeHTML details summary');


Array.from(summary).forEach(btn => {
  btn.addEventListener('click', saveTree);
});

document.addEventListener("DOMContentLoaded", pageReady);


function pageReady(event) {
    let tree = [];
    if (sessionStorage.getItem(STORAGE_NAME) == null || sessionStorage.getItem(STORAGE_NAME) == undefined) {
        sessionStorage.setItem(STORAGE_NAME, tree = JSON.stringify({'tree_open_branches':[]}));
    }
    else {
        tree = JSON.parse(sessionStorage.getItem(STORAGE_NAME));
        for (let branch of tree['tree_open_branches']) {
            for (let details_branch of details) {
                if(details_branch.querySelector('summary a').innerHTML == branch) {
                    details_branch.setAttribute('open', 'open');
                }
            }
        }
    }
}


function saveTree(event) {
    let treeList = [];
    for (let item of details) {
        if(item.hasAttribute('open')) {
            treeList.push(item.querySelector('summary').textContent);
        }
    }
    sessionStorage.setItem(STORAGE_NAME, JSON.stringify({'tree_open_branches': treeList}));
}
