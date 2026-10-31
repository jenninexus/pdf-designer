'use strict';
// Fictional transitions only. No network, upload or submission implementation.
globalThis.transition = kind => {
  const el = document.querySelector('#first_name'), form = el.form;
  switch (kind) {
    case 'push-same-url': history.pushState({step:'B'},'',location.href); break;
    case 'replace-same-url': history.replaceState({step:'B'},'',location.href); break;
    case 'entry-state': navigation.updateCurrentEntry({state:{step:'B'}}); break;
    case 'heading': document.querySelector('h1').firstChild.data='Fictional role B'; break;
    case 'step': document.querySelector('#step').textContent='Contact step B'; break;
    case 'form-action': form.setAttribute('action','/different-role'); break;
    case 'form-id': form.id='changed'; break;
    case 'form-replacement': { const next=form.cloneNode(false); form.replaceWith(next); next.append(...form.childNodes); break; }
    case 'control-replacement': el.replaceWith(el.cloneNode(true)); break;
    case 'control-move': document.querySelector('#other').append(el); break;
    case 'form-owner': el.setAttribute('form','other'); break;
    case 'reverted-dom': el.setAttribute('aria-label','Last name'); el.removeAttribute('aria-label'); break;
    case 'label': el.labels[0].textContent='Last name'; break;
    case 'disabled': el.disabled=true; break;
    case 'readonly': el.readOnly=true; break;
    case 'value': el.value='Other person'; break;
    case 'hash': location.hash='step-b'; break;
    case 'url': history.pushState({},'', '?step=b'); break;
    case 'reload': location.reload(); break;
    case 'navigate': location.assign('/review-transitions.html?new-document'); break;
    case 'event-mutation': el.addEventListener('input',()=>{form.action='/different-role';},{once:true}); break;
    case 'invisible-state': globalThis.fictionalStep='B'; break;
    default: throw Error('Unknown fixture transition: '+kind);
  }
};
