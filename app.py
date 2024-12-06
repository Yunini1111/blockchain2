from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import PostForm, LoginForm, RegistrationForm
from models import db, User, Post
from flask import abort
from flask_cors import CORS


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blockchain.db'
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    blockchain_intro = "Blockchain is a decentralized ledger technology used to securely store and verify data. It enables trustless transactions and forms the backbone of cryptocurrencies like Bitcoin."
    bitcoin_intro = "Bitcoin is the first decentralized cryptocurrency, created in 2009. It operates on blockchain technology and is a peer-to-peer electronic cash system."
    ethereum_intro = "Ethereum is a decentralized, open-source blockchain platform that enables the creation and execution of smart contracts and decentralized applications (dApps). " 
    posts = Post.query.all()  # 獲取所有文章
    return render_template('index.html', 
                           blockchain_intro=blockchain_intro, 
                           bitcoin_intro=bitcoin_intro,
                           ethereum_intro=ethereum_intro,
                           posts=posts)



@app.route('/cryptocurrency/<string:currency>')
def cryptocurrency(currency):
    # 示例數據：你可以將這些改為資料庫查詢
    crypto_details = {
        "bitcoin": {
            "name": "Bitcoin",
            "description": "Bitcoin is the first and most well-known cryptocurrency, created by an anonymous person or group of people using the pseudonym Satoshi Nakamoto. It was introduced in 2008 through a whitepaper titled Bitcoin: A Peer-to-Peer Electronic Cash System which outlined its purpose as a decentralized digital currency that could operate without the need for central authority, such as a bank or government. Bitcoin enables peer-to-peer transactions over the internet, allowing individuals to send and receive funds directly, without intermediaries. Bitcoin operates on a blockchain — a decentralized ledger that records all transactions made on the network. The blockchain is maintained by a network of computers, or nodes, that validate and secure transactions through a process called mining. Mining involves solving complex mathematical problems to add new blocks to the chain, a mechanism that ensures the security and immutability of the ledger. One of Bitcoin's most important features is its limited supply. The total number of Bitcoins that can ever be mined is capped at 21 million, which introduces scarcity and, in theory, acts as a hedge against inflation. As new Bitcoins are mined, the reward for miners decreases over time, a process known as Bitcoin halving. Bitcoin is considered a store of value by many, often referred to as digital gold due to its ability to preserve value over time. It has become increasingly popular as both an investment asset and a means of transferring value across borders. Despite its volatility, Bitcoin has seen growing adoption in mainstream financial markets, with businesses, financial institutions, and even some governments integrating it into their systems. Bitcoin's decentralized nature and the ability to operate without intermediaries have made it a revolutionary technology in the financial world, paving the way for the broader cryptocurrency ecosystem.",
            "image": "static/images/bitcoin.jpg"
        },
        "ethereum": {
            "name": "Ethereum",
            "description": "Ethereum is a decentralized, open-source blockchain platform that enables the creation and execution of smart contracts and decentralized applications (dApps). Unlike Bitcoin, which primarily focuses on peer-to-peer transactions, Ethereum allows developers to build decentralized applications that run on its blockchain.The Ethereum network operates on a technology called smart contracts, which are self-executing contracts with the terms of the agreement directly written into code. These smart contracts automatically execute transactions when certain conditions are met, without the need for intermediaries.Ethereum's native cryptocurrency, Ether (ETH), is used to power the network. It is used as a form of payment for transaction fees and computational services on the Ethereum network, including executing smart contracts. Key features of Ethereum include:Decentralization: Ethereum operates on a decentralized network of nodes, making it less susceptible to censorship and control by any central authority.Smart Contracts: Self-executing code that runs on the Ethereum blockchain to facilitate, verify, or enforce the terms of a contract.dApps: Decentralized applications that run on Ethereum’s blockchain, providing a wide range of use cases from finance (DeFi) to gaming and supply chain management.Ethereum 2.0: An upcoming upgrade to the Ethereum network that aims to improve scalability, security, and energy efficiency through a shift from Proof of Work (PoW) to Proof of Stake (PoS) consensus mechanism.Ethereum is a foundational platform for the burgeoning decentralized finance (DeFi) ecosystem and has inspired the development of many other blockchain projects and applications.",
            "image": "static/images/ethereum.jpg"
        },
        "blockchain": {
            "name": "Blockchain",
            "description": "Blockchain is a distributed ledger technology that ensures secure, transparent, and immutable record-keeping. It allows data to be stored across a decentralized network of computers, known as nodes, instead of being stored in a single centralized database. This decentralized nature makes blockchain highly resistant to tampering and fraud, as any changes to the data require the consensus of the network, making it nearly impossible to alter past transactions. At its core, a blockchain is composed of blocks, which are collections of transactions or data. Each block contains a unique identifier called a hash, a timestamp, and the hash of the previous block, forming a chain of blocks — hence the name blockchain.This structure ensures that once a block is added to the chain, it is virtually impossible to modify without altering every subsequent block, which requires the consensus of the network. Blockchain technology operates on a peer-to-peer network, where each participant has access to the entire blockchain. This transparency enables all participants to view the history of transactions, providing a high level of accountability and trust without the need for intermediaries. The security of blockchain is achieved through cryptography, where each transaction is verified and encrypted before it is added to the chain. One of the key benefits of blockchain is its application in decentralized systems. It eliminates the need for a central authority, such as a bank or government, by allowing users to interact directly with one another in a trustless environment. This feature has led to its widespread adoption in various industries, including finance (e.g., Bitcoin and other cryptocurrencies), supply chain management, healthcare, voting systems, and more. Blockchain's promise lies in its ability to ensure data integrity, streamline processes, and reduce reliance on intermediaries, making it a revolutionary technology that has the potential to transform many industries worldwide.",
            "image": "static/images/blockchain.jpg"
        }
    }
    # 從字典中獲取加密貨幣的詳細信息
    details = crypto_details.get(currency.lower())
    if not details:
        abort(404)  # 若查找不到對應的加密貨幣資訊，返回404錯誤
    return render_template('cryptocurrency.html', details=details)







@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, author=current_user.username, content=form.content.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('index'))
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('view_post', post_id=post.id))
    return render_template('edit_post.html', form=form)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/search_Posts')
def search_Posts():
    query = request.args.get('query', '')
    results = Post.query.filter(Post.title.contains(query)).all()
    return render_template('search_results.html', results=results)

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    comment_data = request.json.get('comment', '')
    # 假設保存到資料庫
    new_comment = Comment(content=comment_data)
    db.session.add(new_comment)
    db.session.commit()
    comments = Comment.query.all()
    comments_html = ''.join([f"<p>{c.content}</p>" for c in comments])
    return jsonify({'comments_html': comments_html})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
