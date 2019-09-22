import { css } from 'lit-element'

export default css`
:host {
    display: flex;
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
    justify-content: center;
    align-items: center;
}

#pageMain {
    border: 1px solid #595959;
    width: 100vw;
    height: 100vh;
    margin: 0 auto;
    padding: 0;
    border-radius: 2px;

    display: grid;
    grid-template-rows: 50px auto 60px;
}

header {
    display: grid;
    grid-template-columns: 100px auto;
    grid-template-rows: 50px;  
    border-bottom: 1px solid #595959;
}

main {
    overflow: scroll;
}

.content {
    height: 150px;
}

.logo, .title, .select-local, .my-local, footer span, .content, .search {
    background-color: #EEEEEE;
    margin: 5px;
    border-radius: 3px;
    color: #999999;
    display: flex;
    justify-content: center;
    align-items: center;
}

.select-local {
    border-radius: 25px;
}

.my-local {
    justify-content: flex-end;
    justify-self: flex-end;
    width: fit-content;
    border-radius: 25px;
}

footer {
    border-top: 1px solid #595959;
}

footer span {
    height: calc(100% - 10px);
    margin: 5px;
}
`
